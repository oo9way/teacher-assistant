from bot.keyboards import replies
from bot.decorator import get_user

@get_user
def start(update, context, user):
    message = """Hello world"""
    update.message.reply_text(message, reply_markup=replies.main_menu())