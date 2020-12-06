from flask import Blueprint
from flask import current_app as app


# Blueprint Configuration
core_bp = Blueprint("core_bp", __name__, template_folder="templates", static_folder="static", url_prefix='')
