from bot.decorator import get_user
from group.models import Group
from bot.utils import notify_admins
from bot.keyboards import inlines
from bot.models import TelegramUser


@get_user
def handle_callback_query(update, context, user):
    query = update.callback_query

    if query.data.startswith("rtj_"):
        group_id = int(query.data.split("_")[1])
        request_to_join(query, context, user, group_id=group_id)

    if query.data.startswith("approve_") or query.data.startswith("reject_"):
        action = "reject" if query.data.startswith("reject_") else "approve"
        group_id = int(query.data.split("_")[2])
        student_id = int(query.data.split("_")[1])
        approve_or_reject_student(query, context, user, action=action, group_id=group_id, student_id=student_id)


def request_to_join(query, context, user, **kwargs):
    group_id = kwargs.get("group_id")
    query.answer()
    try:
        group = Group.objects.get(id=group_id)
        message_to_admin = {
            "text": f"✅ {user.first_name} {user.last_name} {group.name} guruhiga a'zo bo'lish uchun so'rov yubordi",
            "reply_markup": inlines.approve_student(user.telegram_id, group.id)
        }
        notify_admins(context, message_to_admin)
        text = f"✅ \"{group.name}\" guruhiga a'zo bo'lish uchun so'rov yuborildi"
        query.edit_message_text(text=text)
    except Group.DoesNotExist:
        return


def approve_or_reject_student(query, context, user, **kwargs):
    group_id = kwargs.get("group_id")
    student_id = kwargs.get("student_id")
    action = kwargs.get("action")

    try:
        group = Group.objects.get(id=group_id)
        student = TelegramUser.objects.get(telegram_id=student_id)
        if action == "approve":
            group.members.add(student)
            text = f"✅ Guruhga a'zolik tasdiqlandi"
            query.edit_message_text(text=text)
            context.bot.send_message(
                chat_id=student.telegram_id,
                text=f"Guruhga a'zo bo'lish so'rovingiz tasdiqlandi",
            )
            return
        elif action == "reject":
            text = f"❌ Bekor qilindi"
            query.edit_message_text(text=text)
            context.bot.send_message(
                chat_id=student.telegram_id,
                text=f"Guruhga a'zo bo'lish so'rovingiz bekor qilindi",
            )
            return
    except Group.DoesNotExist:
        return
