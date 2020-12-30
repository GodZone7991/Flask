from flask import url_for
from .bot import bot, TELEGRAM_CACHES, BASE_URL
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
)
import json
from application import utils

USER_INFO_TEMPLATE = {'user_id': '',  # user telegram id
                      'logged_in': 0,  # True-False value
                      'spotify_id': '',
                      'spotify_session': '',
                      'current_status': 0,  # status code for future features
                      }

# initialisation of an updater instance and a dispatcher one for it
updater = Updater(bot=bot)
dispatcher = updater.dispatcher


def create_cache(user):
    file = TELEGRAM_CACHES + f'{user}'
    with open(file, 'w+', encoding='utf-8') as cache:
        json.dump(USER_INFO_TEMPLATE, cache)


def callback(chat_id):
    bot.send_message(chat_id=chat_id, text='U have successfully logged in')


def start(update, context):
    user = f'{update.effective_chat.id}'
    file = TELEGRAM_CACHES + user
    create_cache(user)
    utils.add_cache_data(file, user_id=user)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello there!")


def login(update, context):
    user = update.effective_chat.id

    context.bot.send_message(
        chat_id=user,
        text=''.join(
            (BASE_URL,
             url_for('spotify_bp.login'),
             f'?telegram-id={user}')
        ))


def test(update, context):
    update.message.reply_text(update.message.text)


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('login', login))
dispatcher.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, test))
