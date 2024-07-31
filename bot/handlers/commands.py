from bot.keyboards import replies

def start(update, context):
    message = "Assalamu alaykum, botga xush kelibsiz"
    update.message.reply_text(message, reply_markup=replies.main_menu())