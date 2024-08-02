from bot.models import TelegramUser


def get_user(func):
    def wrapper(update, context, *args, **kwargs):
        user = update.message.from_user
        first_name = user.first_name
        last_name = user.last_name
        telegram_id = user.id

        user, _ = TelegramUser.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={
                "first_name": first_name,
                "last_name": last_name
                }
        )
        return func(update, context, user, *args, **kwargs)
    return wrapper