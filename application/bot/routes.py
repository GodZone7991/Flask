from .bot import bot_bp, bot
from .bot_manager import dispatcher
import telegram
from flask import render_template, request, make_response
from application.config import TG_BOT_TOKEN

# TODO: логин пользователя в спотифай
# TODO: есть длинный список жанров, который нужно упростить: обоб
# TODO: механизм оценки треков из заготовленной нами подборки
# TODO: механизм сохранения лайкнутых треков, находящихся в плейлисте в персонализированные рекомендации
# TODO: генерация плейлиста на основе сида из персонализированных рекомендаций в нашей БД


@bot_bp.route("/", methods=["GET", "POST"])
def home():
    """Indexing page with info about a bot"""
    if request.method == "POST":
        return render_template(
            'index.html',
            title="PsyMusic Bot",
            body=request.json
        )
    return render_template(
        'index.html',
        title="PsyMusic Bot",
        body='Саня хуй соси'
    )


@bot_bp.route("/{}".format(TG_BOT_TOKEN), methods=["POST"])
def get_message():
    """
    The function accepts messages from telegram.
    :return: make_response()
    """
    if request.method == "POST":
        update = telegram.update.Update.de_json(request.json, bot)
        dispatcher.process_update(update)
        return make_response(request.json, 200)
    return make_response('Method not allowed', 405)
