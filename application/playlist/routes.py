import spotipy
from flask import request, make_response, jsonify, request
from application.config import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
from spotipy.oauth2 import SpotifyClientCredentials
from application.core.models import db, Track
from sqlalchemy import exc
from .playlist import playlist_bp


auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(auth_manager=auth_manager)


@playlist_bp.route('/parse', methods=['GET'])
def parse_playlist():

    """
    This function expect two args: playlist id and mood label. It find playlist by Spotify API, get track's features
    list, and set a mood label to every track in it. After all it saves the added playlist to the DB.
    """

    if request.values is None:
        return
    results = spotify.playlist(request.args['playlist'], fields=None, market=None, additional_types=('track',))
    results = results['tracks']['items']
    ids = [item['track']['id'] for item in results]
    features = spotify.audio_features(tracks=ids)
    for index, item in enumerate(features):
        track = Track(name=results[index]['track']['name'],
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
                      mood_label=request.args['mood'])
        set_fields = track.__dict__.copy()
        del set_fields['_sa_instance_state']
        try:
            db.session.add(track)
            db.session.commit()
        except exc.IntegrityError or exc.InvalidRequestError:
            db.session.rollback()
            changed_track = Track.query.filter_by(track_id=ids[index]).update(set_fields)
            db.session.commit()

    # TODO: decompose this shit
    return make_response(jsonify(features), 200)


@playlist_bp.route('/get_playlist', methods=['GET'])
def get_playlist():
    params = len(request.values)
    print(params)
    response = 'params'
    # response = spotify.recommendations(limit=100, **params)
    return make_response(response, 200)
