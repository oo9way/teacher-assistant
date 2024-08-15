from bot.keyboards import replies
from bot.keyboards.inlines import inline_groups
from bot.decorator import get_user
from bot import states


@get_user
def start(update, context, user):
    student = not user.is_teacher
    if student:
        groups = user.groups.all()
        if not inline_groups("rtj")['inline_keyboard'][0]:
            update.message.reply_text("Hozirda aktiv guruhlar mavjud emas.")
            return None

        if not groups:
            update.message.reply_text("Siz hech qanday guruhga a'zo emassiz. A'zo bo'lish uchun so'rov yuboring.",
                                      reply_markup=inline_groups("rtj"))
            return None

        message = "Assalamu alaykum, botga xush kelibsiz"
        update.message.reply_text(message, reply_markup=replies.student_main())

    if not student:
        selected_group = context.user_data.get("selected_group", None)
        if not selected_group:
            update.message.reply_text("Guruhni tanlang.", reply_markup=inline_groups(key="selectedgroup"))
            return states.END

        update.message.reply_text("Kerakli bo'limni tanlang.", reply_markup=replies.teacher_main())
