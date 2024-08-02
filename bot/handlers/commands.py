from bot.keyboards import replies
from bot.decorator import get_user

@get_user
def start(update, context, user):
    message = """
    Ассалому алайкум. \nМен 'Eleven Wаter' етказиб бериш хизмати ботиман! \nКеракли хизматни танланг!
    """
    update.message.reply_text(message, reply_markup=replies.main_menu())