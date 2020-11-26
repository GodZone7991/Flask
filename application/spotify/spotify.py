from flask import Blueprint
from flask import current_app as app


# Blueprint Configuration
spotify_bp = Blueprint(
    "spotify_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/spotify'
)

from . import routes
