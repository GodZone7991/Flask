from flask import Blueprint
from application.config import TG_BOT_TOKEN
from flask import current_app as app
import telegram
from telegram.ext import Updater, CommandHandler


# Blueprint Configuration
bot_bp = Blueprint(
    "bot_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/bot'
)
bot = telegram.Bot(token=TG_BOT_TOKEN)
updater = Updater(bot=bot)
from . import bot_manager

bot_manager.dispatcher.add_handler(CommandHandler('start', bot_manager.start))
from . import routes
