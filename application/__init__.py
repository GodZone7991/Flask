from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import application.config as config
from flask_migrate import Migrate
from flask_sessions import Session


db = SQLAlchemy()
migrate = Migrate()
session = Session()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config.DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db, directory='migrations')
    session.init_app(app)

    with app.app_context():
        from application.core.core import core_bp
        from .core import routes as core_routes
        from .bot.bot import bot_bp
        from .bot import routes as bot_routes
        from .spotify.spotify import spotify_bp
        from .spotify import routes as spotify_routes
        db.create_all()  # Create sql tables for our data models
        app.register_blueprint(core_bp)
        app.register_blueprint(bot_bp)
        app.register_blueprint(spotify_bp)
        return app
