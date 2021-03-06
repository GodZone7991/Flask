from flask import Blueprint, current_app as app
from application.config import SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID
from application import utils


# TODO: Интерфейс парсинга плейлиста
# TODO: Интерфейс сохранения данных парсинга в БД
# TODO: Интерфейс вызова данных из БД и составления запроса к API
# TODO: Интрефейс обработки ответа API и сохранения в БД
# TODO: Интерфейс передачи из БД в сисетему ML
# TODO: Интерфейс приема данных от ML и записи в БД (mood set)
# TODO: Интерфейс генерации плейлиста для пользователя на основе mood set'а из БД


SPOTIFY_CACHES = './.spotify_caches/'
SPOTIFY_REDIRECT_URI = app.config['SPOTIFY_REDIRECT_URI']

SPOTIFY_PARAMS = {
    'client_id': SPOTIFY_CLIENT_ID,
    'client_secret': SPOTIFY_CLIENT_SECRET,
    'redirect_uri': SPOTIFY_REDIRECT_URI,
    'scope': ','.join([
        'user-read-recently-played',
        'user-top-read',
        'user-library-read',
        'playlist-modify-private',
        'playlist-modify-public',
    ])
}


# Blueprint Configuration
spotify_bp = Blueprint(
    "spotify_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/spotify')


utils.create_caches(SPOTIFY_CACHES)
