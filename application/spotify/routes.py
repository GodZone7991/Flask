import spotipy
from flask import request, make_response, jsonify, request
from application.config import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
from spotipy.oauth2 import SpotifyOAuth
from application.core.models import db, Track
from sqlalchemy import exc
from .spotify import spotify_bp

# TODO: Make user login function


auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri='http://127.0.0.1:5000/')
spotify = spotipy.Spotify(auth_manager=auth_manager)


def save_tracks(features: dict, track_info: dict) -> str:
    """
    This function accepts two dicts: features contains audio-features from Spotify,
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


@spotify_bp.route('/parse_playlist', methods=['GET'])
def parse_playlist() -> make_response():

    """
    This view expect two request parameters: spotify id and mood label. It find spotify by Spotify API, get track's
    features list, and set a mood label to every track in it. After all it saves the added track to the DB.
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
    This function accepts a sequence of http parameters for filtering Spotify's recommendation query.
    One of required parameters is seed_genres, seed_tracks or seed_artists. Rest are used for filtering and unnecessary.
    :return: make_response(status, code)
    """
    # TODO: make a returning value of this function more informative and adaptive; make error handlers
    params = request.values
    print(params)
    response = 'params'
    response = spotify.recommendations(limit=100, **params)
    return make_response(response, 200)
