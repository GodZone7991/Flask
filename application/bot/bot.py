from flask import Blueprint
from application.config import TG_BOT_TOKEN, BASE_URL
from telegram import Bot
from telegram.ext import Updater
import logging
from application import utils


TELEGRAM_CACHES = './.telegram_caches/'
TELEGRAM_FILES = './.telegram_files/'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


logger = logging.getLogger(__name__)


# register blueprint
bot_bp = Blueprint("bot_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/bot')


# create a directory for cache
utils.create_caches(TELEGRAM_CACHES)
utils.create_caches(TELEGRAM_FILES)


# create a bot instance
bot = Bot(token=TG_BOT_TOKEN)
updater = Updater(bot=bot)
dispatcher = updater.dispatcher
