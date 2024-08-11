from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler

from bot.handlers import commands, commons, queries
from bot import states

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

dispatcher = Dispatcher(bot, None, workers=0)

dispatcher.add_handler(CommandHandler("start", commands.start))
dispatcher.add_handler(CallbackQueryHandler(queries.handle_callback_query))
dispatcher.add_handler(MessageHandler(Filters.text, commons.echo))
