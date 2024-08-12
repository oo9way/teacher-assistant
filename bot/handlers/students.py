from bot.decorator import get_user
from telegram import ReplyKeyboardRemove
from bot.keyboards import replies, inlines
from student.models import StudentTask


@get_user
def get_lessons(update, context, user):
    lessons = user.groups.first().finished_lessons.all()

    if not lessons:
        update.message.reply_text("Siz a'zo bo'lgan guruhda darslar hali boshlanmadi.",
                                  reply_markup=replies.student_main())
        return None

    message = "👨‍💻 Darslar:\n\n"
    for lesson in lessons:
        message += f"<a href='http://127.0.0.1:8000/admin/group/group/'>{lesson.title}</a>\n"

    update.message.reply_text(message, parse_mode="HTML", reply_markup=replies.student_main())
    return None


@get_user
def get_uncompleted_tasks(update, context, user):
    student_tasks = StudentTask.objects.filter(student=user, is_completed=False)

    if not student_tasks:
        message = "✅ Sizda bajarilmagan topshiriqlar mavjud emas. "
        update.message.reply_text(message, reply_markup=replies.student_main())
        return None

    message = "<b>📖 Bajarilmagan topshiriqlar:</b>\n\n"
    counter = 1
    for task in student_tasks:
        message += f"{counter}. {task.task.body[:100]}\n"
        counter += 1

    update.message.reply_text(message, parse_mode="HTML", reply_markup=inlines.uncompleted_tasks(student_tasks))
    return None
