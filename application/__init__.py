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
    migrate.init_app(app, db,)

    with app.app_context():
        from . import routes  # Import routes
        db.create_all()  # Create sql tables for our data models

        return app
