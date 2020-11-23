from flask import Blueprint
from flask import current_app as app


# Blueprint Configuration
playlist_bp = Blueprint(
    "playlist_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/playlist'
)

from . import routes
