from flask import Blueprint
from flask import current_app as app

# Blueprint Configuration
bot_bp = Blueprint(
    "bot_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/bot'
)

from . import routes