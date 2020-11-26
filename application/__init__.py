from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import application.config as config
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config.DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db, directory='migrations')

    with app.app_context():
        from application.core.core import core_bp
        from .bot.bot import bot_bp
        from .spotify.spotify import spotify_bp
        db.create_all()  # Create sql tables for our data models
        app.register_blueprint(core_bp)
        app.register_blueprint(bot_bp)
        app.register_blueprint(spotify_bp)
        return app

# TODO: Интерфейс парсинга плейлиста
# TODO: Интерфейс сохранения данных парсинга в БД
# TODO: Интерфейс вызова данных из БД и составления запроса к API
# TODO: Интрефейс обработки ответа API и сохранения в БД
# TODO: Интерфейс передачи из БД в сисетему ML
# TODO: Интерфейс приема данных от ML и записи в БД (mood set)
# TODO: Интерфейс генерации плейлиста для пользователя на основе mood set'а из БД
# TODO: продумать модель с использованием прокси-параметров для поиска в базе spotify
# TODO: опробовать модель с избыточным числом параметров
# TODO: Посмотреть документацию к TensorFlow, прикрутить тест оценки настроения,
