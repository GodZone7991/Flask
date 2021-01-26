import spotipy
from application.core.models import db, Track
from sqlalchemy import exc
from .spotify import SPOTIFY_PARAMS, SPOTIFY_CACHES
from application.bot.bot import TELEGRAM_CACHES
from application import utils


def initialize_spotify(session):
    auth_manager = spotipy.SpotifyOAuth(**SPOTIFY_PARAMS)
    auth_manager.cache_path = SPOTIFY_CACHES + session
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify


def login(session, redir_url='spotify_bp.login', code=None):
    auth_manager = spotipy.SpotifyOAuth(**SPOTIFY_PARAMS)
    auth_manager.cache_path = SPOTIFY_CACHES + session
    if code is None and auth_manager.get_cached_token() is None:
        return auth_manager.get_authorize_url()
    if code:
        auth_manager.get_access_token(code=code)
        return redir_url
    return redir_url


def get_user_info(session):
    spotify = initialize_spotify(session)
    user_info = spotify.me()
    return user_info


def save_tracks(features: list, track_info: list, mood: str) -> str:
    """
    This function accepts two lists: features contain audio-features from Spotify,
    track-info contains pairs of ids and names of track, and one string, that sets a mood.
    In result, the function saves info about tracks into the DB.
    :return: status: str
    """
    # TODO: add status as returning value for better logging and testing; make better error handlers
    for index, item in enumerate(features):
        name = track_info[index][1]
        headers = {'name': name,
                   'track_id': item['id'],
                   'danceability': item['danceability'],
                   'energy': item['energy'],
                   'key': item['key'],
                   'loudness': item['loudness'],
                   'mode': item['mode'],
                   'speechiness': item['speechiness'],
                   'acousticness': item['acousticness'],
                   'instrumentalness': item['instrumentalness'],
                   'liveness': item['liveness'],
                   'valence': item['valence'],
                   'tempo': item['tempo'],
                   'mood_label': mood}
        track = Track(**headers)
        db.session.add(track)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            del headers['track_id']
            Track.query.filter(Track.track_id == track_info[index][0]).update(headers)
            db.session.commit()
    return 'OK!'


def parse_playlist(session: str, playlist_id: str):

    """
    This view expect two request parameters: spotify id and mood label. It finds spotify playlist by Spotify API and
    gets track's features list. It returns a tuple with the json-like features sequence and a dict with id's and names
    of gotten tracks.
    :return: tuple(features, track_list)
    """
    limit = 100
    counter = 0
    offset = limit * counter
    track_list = []
    spotify = initialize_spotify(session)
    playlist = spotify.playlist_items(
        playlist_id,
        fields='items.track.id, items.track.name, total',
        market=None,
        offset=offset,
        additional_types=('track',))
    features = spotify.audio_features(tracks=[item['track']['id'] for item in playlist['items']])
    track_list += [[item['track']['id'], item['track']['name']] for item in playlist['items']]
    counter += 1
    rest = playlist['total'] - limit
    while rest > 0:
        offset = limit * counter
        playlist = spotify.playlist_items(
            playlist_id,
            fields='items.track.id, items.track.name, total',
            market=None,
            additional_types=('track',),
            offset=offset)
        features = spotify.audio_features(tracks=[item['track']['id'] for item in playlist['items']])
        track_list += [[item['track']['id'], item['track']['name']] for item in playlist['items']]
        rest -= offset
    return features, track_list


def get_tracks_data(**kwargs):
    tracks = Track.query.filter(Track.mood_label == kwargs['mood']).all()
    tracks = [track.get_json() for track in tracks]
    return tracks


def get_user_top_tracks(session: str):
    spotify = initialize_spotify(session)
    user_top_tracks = spotify.current_user_top_tracks(limit=100, time_range='long_term')
    return user_top_tracks


def get_features_for_track_list(session: str, track_id_list: list):
    spotify = initialize_spotify(session)
    features = spotify.audio_features(track_id_list)
    return features


def save_user_top_features(user: str, features: list):
    cache_file = ''.join([TELEGRAM_CACHES, user])
    utils.add_cache_data(cache_file, features=features)

