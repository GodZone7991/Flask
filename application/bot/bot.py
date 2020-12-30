from flask import Blueprint
from application.config import TG_BOT_TOKEN, BASE_URL
import telegram
import logging
from application import utils


TELEGRAM_CACHES = './.telegram_caches/'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


logger = logging.getLogger(__name__)


# register blueprint
bot_bp = Blueprint("bot_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/bot')


# create a directory for cache
utils.create_caches(TELEGRAM_CACHES)


# create a bot instance
bot = telegram.Bot(token=TG_BOT_TOKEN)
