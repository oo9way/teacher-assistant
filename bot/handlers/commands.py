from bot.keyboards import replies
from bot.keyboards.inlines import inline_groups
from bot.decorator import get_user


@get_user
def start(update, context, user):
    student = not user.is_teacher
    if student:
        groups = user.groups.all()
        if not inline_groups()['inline_keyboard'][0]:
            update.message.reply_text("Hozirda aktiv guruhlar mavjud emas.")
            return None

        if not groups:
            update.message.reply_text("Siz hech qanday guruhga a'zo emassiz. A'zo bo'lish uchun so'rov yuboring.",
                                      reply_markup=inline_groups())
            return None

        message = "Assalamu alaykum, botga xush kelibsiz"
        update.message.reply_text(message, reply_markup=replies.student_main())
