import spotipy
from flask import current_app as app
from flask import request, make_response, jsonify, request, redirect, url_for, session
from application.config import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID, SPOTIFY_REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth
from application.core.models import db, Track
from sqlalchemy import exc
from .spotify import spotify_bp
import os
import uuid


# TODO: Make user login function


spotify = spotipy.Spotify()


caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')


def save_tracks(features: dict, track_info: dict) -> str:
    """
    This function accepts two dicts: features contain audio-features from Spotify,
    track-info contains pairs of ids and names of track. In result, the function saves
    info about tracks into the DB.
    :return: status: str
    """
    # TODO: add status as returning value for better logging and testing; make better error handlers
    for index, item in enumerate(features):
        track = Track(
            name=track_info[index]['track']['name'],
            track_id=item['id'],
            danceability=item['danceability'],
            energy=item['energy'],
            key=item['key'],
            loudness=item['loudness'],
            mode=item['mode'],
            speechiness=item['speechiness'],
            acousticness=item['acousticness'],
            instrumentalness=item['instrumentalness'],
            liveness=item['liveness'],
            valence=item['valence'],
            tempo=item['tempo'],
            mood_label=request.args['mood'],
        )
        set_fields = track.__dict__.copy()
        del set_fields['_sa_instance_state']
        try:
            db.session.add(track)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            Track.query.filter_by(track_id=track_info[index]).update(set_fields)
            db.session.commit()
    return 'OK!'


@spotify_bp.route('/account', methods=['GET'])
def login():
    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())
    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI + 'spotify/account',
        cache_path=session_cache_path())
    if 'code' in request.args:
        code = request.args.get('code')
        auth_manager.get_access_token(code=code)
        return redirect(url_for('spotify_bp.login'))
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return make_response(spotify.me(), 400)


@spotify_bp.route('/parse_playlist', methods=['GET'])
def parse_playlist() -> make_response():

    """
    This view expect two request parameters: spotify id and mood label. It finds spotify playlist by Spotify API, gets
    track's features list, and sets a mood label to every track in it. After all it saves the added track to the DB.
    :return: make_response(status, code)
    """

    if request.args.get('playlist') is None:
        return make_response('No arguments transmitted', 200)
    playlist = spotify.playlist(request.args['playlist'], fields=None, market=None, additional_types=('track',))
    playlist = playlist['tracks']['items']
    track_list = {item['track']['id']: item['track']['name'] for item in playlist}
    features = spotify.audio_features(tracks=track_list)
    save_tracks(features, track_list)
    return make_response(jsonify(features), 200)


@spotify_bp.route('/get_recommendations', methods=['GET'])
def get_playlist() -> make_response():
    """
    This function accepts a sequence of http parameters for filtering of Spotify's recommendation query.
    One of required parameters is either seed_genres or seed_tracks or seed_artists. Rest are used for filtering and
    aren't necessary.
    :return: make_response(status, code)
    """
    # TODO: make a returning value of this function more informative and adaptive; make error handlers
    params = request.values
    print(params)
    response = 'params'
    response = spotify.recommendations(limit=100, **params)
    return make_response(response, 200)
