from flask import Blueprint
from application.config import TG_BOT_TOKEN
from flask import current_app as app
import telegram
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# register blueprint
bot_bp = Blueprint("bot_bp", __name__, template_folder="templates", static_folder="static", url_prefix='/bot')

# create a bot instance
bot = telegram.Bot(token=TG_BOT_TOKEN)
