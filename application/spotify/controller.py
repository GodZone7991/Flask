import spotipy
from application.core.models import db, Track
from sqlalchemy import exc
from .spotify import SPOTIFY_PARAMS, CACHES_FOLDER


def initialize_spotify(session):
    auth_manager = spotipy.SpotifyOAuth(**SPOTIFY_PARAMS)
    auth_manager.cache_path = CACHES_FOLDER + session
    spotify = spotipy.Spotify(auth_manager)
    return spotify


def login(session, redir_url='spotify_bp.login', code=None):
    auth_manager = spotipy.SpotifyOAuth(**SPOTIFY_PARAMS)
    auth_manager.cache_path = CACHES_FOLDER + session
    if code is None and auth_manager.get_cached_token() is None:
        return auth_manager.get_authorize_url()
    if code:
        auth_manager.get_access_token(code=code)
        return redir_url
    return redir_url


def save_tracks(features: dict, track_info: dict, mood: str) -> str:
    """
    This function accepts two dicts: features contain audio-features from Spotify,
    track-info contains pairs of ids and names of track, and one string, that sets a mood.
    In result, the function saves info about tracks into the DB.
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
            mood_label=mood,
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


def parse_playlist(playlist_id: str, session: str, spotify=initialize_spotify):

    """
    This view expect two request parameters: spotify id and mood label. It finds spotify playlist by Spotify API and
    gets track's features list. It returns a tuple with the json-like features sequence and a dict with id's and names
    of gotten tracks.
    :return: tuple(features, track_list)
    """
    spotify = spotify(session)
    playlist = spotify.playlist(playlist_id, fields=None, market=None, additional_types=('track',))
    playlist = playlist['tracks']['items']
    track_list = {item['track']['id']: item['track']['name'] for item in playlist}
    features = spotify.audio_features(tracks=track_list)
    return features, track_list


def get_playlist(session: str, spotify=initialize_spotify, **kwargs):
    """

    :return:
    """
    # TODO: make a returning value of this function more informative and adaptive; make error handlers
    spotify = spotify(session)
    params = kwargs
    print(kwargs)
    return f'{spotify}, {kwargs}'
