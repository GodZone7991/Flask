from flask import url_for
import requests
from .bot import bot, TELEGRAM_CACHES, BASE_URL, TELEGRAM_FILES
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
)
from application import utils

USER_INFO_TEMPLATE = {'user_id': '',  # user telegram id
                      'logged_in': 0,  # True-False value
                      'spotify_id': '',
                      'spotify_session': '',
                      'current_status': 0,  # status code for future features
                      }


AVAILABLE_FORMATS = 'json', 'csv'
AVAILABLE_MOODS = 'aggressive', 'depressive', 'chill', 'happy'


# initialisation of an updater instance and a dispatcher one for it
updater = Updater(bot=bot)
dispatcher = updater.dispatcher


def callback(chat_id, text="You"):
    bot.send_message(chat_id=chat_id, text=f"{text} successfully logged in")


def start(update, context):
    user = f'{update.effective_chat.id}'
    file = ''.join((TELEGRAM_CACHES, user))
    data = USER_INFO_TEMPLATE.copy()
    data['user_id'] = user
    if utils.check_existence(file):
        context.bot.send_message(chat_id=update.effective_chat.id, text="You've already started")
    else:
        utils.write_cache(file, data)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello there!")


def login(update, context):
    user = f'{update.effective_chat.id}'
    cached_data = utils.read_cache(''.join([TELEGRAM_CACHES, user]))
    if cached_data['logged_in']:
        context.bot.send_message(chat_id=user, text=f"You've already logged in as {cached_data['spotify_name']}")
    else:
        context.bot.send_message(
            chat_id=user,
            text=''.join(
                (BASE_URL,
                 url_for('spotify_bp.login'),
                 f'?telegram-id={user}')
            ))


def test(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def update_track_data(update, context):
    spotify_uri, mood = context.args
    user = update.effective_chat.id
    payload = {'mood': mood, 'playlist': spotify_uri.split(':').pop(), 'user': user}
    data = requests.request('GET', ''.join([BASE_URL, url_for('spotify_bp.parse_playlist')]), params=payload).json()
    context.bot.send_message(chat_id=user, text=data['text'])
    return


def get_track_data(update, context):
    payload = {'mood': context.args[0], 'format': context.args[1]}
    mood = payload['mood']
    file_format = payload['format']
    if mood not in AVAILABLE_MOODS or file_format not in AVAILABLE_FORMATS:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Wrong parameters')
        return
    file_name = ''.join([TELEGRAM_FILES, f'{mood}.{file_format}'])
    if not utils.check_existence(file_name):
        data = requests.request('GET', ''.join([BASE_URL, url_for('spotify_bp.get_tracks')]), params=payload).json()
        print(data), print(type(data))
        utils.write_cache(file_name, data, file_format=file_format)
    with open(file_name, mode='rb') as file:
        context.bot.send_document(chat_id=update.effective_chat.id, document=file, filename=f'{mood}.{file_format}')
    return


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('login', login))
dispatcher.add_handler(CommandHandler('get_tracks', get_track_data, pass_args=True))
dispatcher.add_handler(CommandHandler('update_tracks', update_track_data, pass_args=True))
dispatcher.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, test))
