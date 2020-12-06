from flask import Blueprint
from flask import current_app as app


# Blueprint Configuration
spotify_bp = Blueprint(
    "spotify_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/spotify')

# TODO: Интерфейс парсинга плейлиста
# TODO: Интерфейс сохранения данных парсинга в БД
# TODO: Интерфейс вызова данных из БД и составления запроса к API
# TODO: Интрефейс обработки ответа API и сохранения в БД
# TODO: Интерфейс передачи из БД в сисетему ML
# TODO: Интерфейс приема данных от ML и записи в БД (mood set)
# TODO: Интерфейс генерации плейлиста для пользователя на основе mood set'а из БД
