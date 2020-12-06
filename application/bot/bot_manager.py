from .bot import bot
from telegram.ext import Updater, CommandHandler

# initialisation of an updater instance and a dispatcher one for it
updater = Updater(bot=bot)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="САНЯ ХУЙ СОСИ")


dispatcher.add_handler(CommandHandler('start', start))
