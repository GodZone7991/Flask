import spotipy
from application.core.models import db, Track
from sqlalchemy import exc
from .spotify import SPOTIFY_PARAMS, SPOTIFY_CACHES
from application.utils import UserCache


class Manager:
    cache_path = SPOTIFY_CACHES

    def __init__(self, user: UserCache):
        self.session = user.cached_data.get('spotify_session')
        self.user_id = user.cached_data.get('spotify_id')
        self._auth_manager = spotipy.SpotifyOAuth(**SPOTIFY_PARAMS, cache_path=''.join([self.cache_path, self.session]))
        self.spotify = self.__initialize_spotify()

    def __initialize_spotify(self):
        auth_manager = self._auth_manager
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        return spotify

    @property
    def authorize_url(self):
        return self._auth_manager.get_authorize_url()

    def get_user_top_tracks(self):
        user_top_tracks = self.spotify.current_user_top_tracks(limit=50, time_range='long_term')
        user_top_tracks = [track['id'] for track in user_top_tracks['items']]
        return user_top_tracks

    def parse_playlist(self, playlist_id: str):
        """
        :return: tuple(features, track_list)
        """
        track_list = []
        features = []

        def inner(offset: int = 0, counter: int = 0, limit: int = 100, *, rest: int = 0):
            nonlocal track_list, features
            playlist = self.spotify.playlist_items(
                playlist_id,
                fields='items.track.id, items.track.name, total',
                market=None,
                offset=offset,
                additional_types=('track',))
            rest = rest - offset
            if rest < 0:
                return
            elif rest == 0:
                rest = playlist['total']
            counter += 1
            features += self.spotify.audio_features(tracks=[item['track']['id'] for item in playlist['items']])
            track_list += [[item['track']['id'], item['track']['name']] for item in playlist['items']]
            return inner(offset=counter * limit, counter=counter, rest=rest)

        inner()
        return features, track_list

    def get_recommendations(self, artists: tuple = (), genres: tuple = (), tracks: tuple = (), **kwargs):
        recommendations = self.spotify.recommendations(
            seed_artists=artists, seed_genres=genres, seed_tracks=tracks, limit=30, **kwargs)
        recommendations = {
            'seeds': recommendations['seeds'],
            'tracks':
                [
                    {'artists':
                        [
                            {'name': artist['name'], 'id': artist['id'], 'uri': artist['uri']}
                            for artist in track['artists']
                        ],
                        'name': track['name'], 'id': track['id'], 'uri': track['uri']}
                    for track in recommendations['tracks']
                ]
        }
        return recommendations

    def create_playlist(self, mood: str):
        playlist_name = f'{mood.capitalize()} tracks for you'
        description = f'Special tracks for your {mood} mood'
        playlist = self.spotify.user_playlist_create(self.user_id, playlist_name, public=False, description=description)
        return playlist['id']


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


def get_tracks_data(**kwargs):
    tracks = Track.query.filter(Track.mood_label == kwargs['mood']).all()
    tracks = [track.get_json() for track in tracks]
    return tracks
