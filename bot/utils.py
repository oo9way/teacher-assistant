from bot.models import TelegramUser


def notify_admins(context, message):
    admins = TelegramUser.objects.filter(is_teacher=True)
    for admin in admins:
        context.bot.send_message(chat_id=admin.telegram_id, **message)