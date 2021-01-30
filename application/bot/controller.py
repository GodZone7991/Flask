from flask import url_for
import requests
import uuid
import telegram
from .bot import bot, BASE_URL, TELEGRAM_FILES, dispatcher
from telegram.ext import CommandHandler, MessageHandler, filters
from application import utils
from application.spotify import controller


AVAILABLE_FORMATS = 'json', 'csv'
AVAILABLE_MOODS = 'aggressive', 'depressive', 'chill', 'happy'


def callback(chat_id, text="undefined"):
    bot.send_message(chat_id=chat_id, text=text)


def start(update: telegram.Update, context: telegram.ext.CallbackContext):
    user = utils.UserCache(f'{update.effective_user.id}')
    data = {'user_id': user.user_id, 'logged_in': 0, 'spotify_id': '', 'current_status': 0, 'spotify_session': str(uuid.uuid4())}
    if user.is_exist():
        context.bot.send_message(chat_id=update.effective_chat.id, text="You've already started")
    else:
        user.write_cache(data)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello there!")


def login(update: telegram.Update, context: telegram.ext.CallbackContext):
    user = utils.UserCache(f'{update.effective_chat.id}')
    print(user)
    if user.cached_data['logged_in']:
        context.bot.send_message(
            chat_id=user.user_id,
            text=f"You've already logged in as {user.cached_data['spotify_name']}")
    else:
        context.bot.send_message(
            chat_id=user.user_id,
            text=''.join(
                (BASE_URL,
                 url_for('spotify_bp.login'),
                 f'?telegram-id={user.user_id}')
            ))


def test(update: telegram.Update, context: telegram.ext.CallbackContext):
    print(update.effective_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def update_track_data(update: telegram.Update, context: telegram.ext.CallbackContext):
    spotify_uri, mood = context.args
    user = update.effective_chat.id
    payload = {'mood': mood, 'playlist': spotify_uri.split(':').pop(), 'user': user}
    data = requests.request('GET', ''.join([BASE_URL, url_for('spotify_bp.parse_playlist')]), params=payload).json()
    context.bot.send_message(chat_id=user, text=data['text'])
    return


def get_track_data(update: telegram.Update, context: telegram.ext.CallbackContext):
    payload = {'mood': context.args[0], 'format': context.args[1]}
    mood = payload['mood']
    file_format = payload['format']
    if mood not in AVAILABLE_MOODS or file_format not in AVAILABLE_FORMATS:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Wrong parameters')
        return
    file_name = ''.join([TELEGRAM_FILES, f'{mood}.{file_format}'])
    if not utils.check_existence(file_name):
        data = requests.request('GET', ''.join([BASE_URL, url_for('spotify_bp.get_tracks')]), params=payload).json()
        utils.write_file(file_name, data, file_format=file_format)
    with open(file_name, mode='rb') as file:
        context.bot.send_document(chat_id=update.effective_chat.id, document=file, filename=f'{mood}.{file_format}')
    return


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('login', login))
dispatcher.add_handler(CommandHandler('get_tracks', get_track_data, pass_args=True))
dispatcher.add_handler(CommandHandler('update_tracks', update_track_data, pass_args=True))
dispatcher.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, test))
