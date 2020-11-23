from .bot import bot_bp
from flask import render_template


@bot_bp.route("/", methods=["GET"])
def home():
    """Indexing page with info about a bot"""
    return render_template(
        'index.html',
        title="PsyMusic Bot",
    )
