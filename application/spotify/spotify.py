from flask import Blueprint
from application.config import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID, SPOTIFY_REDIRECT_URI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# from flask import current_app as app
import os


CACHES_FOLDER = './.spotify_caches/'


SPOTIFY_PARAMS = {
    'client_id': SPOTIFY_CLIENT_ID,
    'client_secret': SPOTIFY_CLIENT_SECRET,
    'redirect_uri': SPOTIFY_REDIRECT_URI,
}


def create_caches():
    if not os.path.exists(CACHES_FOLDER):
        os.makedirs(CACHES_FOLDER)


# Blueprint Configuration
spotify_bp = Blueprint(
    "spotify_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/spotify')


create_caches()



# TODO: Интерфейс парсинга плейлиста
# TODO: Интерфейс сохранения данных парсинга в БД
# TODO: Интерфейс вызова данных из БД и составления запроса к API
# TODO: Интрефейс обработки ответа API и сохранения в БД
# TODO: Интерфейс передачи из БД в сисетему ML
# TODO: Интерфейс приема данных от ML и записи в БД (mood set)
# TODO: Интерфейс генерации плейлиста для пользователя на основе mood set'а из БД
