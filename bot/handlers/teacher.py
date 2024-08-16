from bot.keyboards import inlines, replies
from bot.decorator import get_user
from group.models import Group
from course.models import Lesson, Task
from student.models import StudentTask
from bot import states


@get_user
def get_groups(update, context, user):
    update.message.reply_text("Guruhni tanlang.", reply_markup=inlines.inline_groups(key="selectedgroup"))


@get_user
def get_tasks(update, context, user):
    group = Group.objects.get(id=context.user_data["selected_group"])
    lessons = group.finished_lessons.all()

    if not lessons:
        update.message.reply_text("Ushbu guruhda darslar hali boshlanmadi.", reply_markup=replies.teacher_main())
        return states.END

    message = "📖 Kerakli darsni tanlang"
    update.message.reply_text(message, parse_mode="html", reply_markup=replies.back_btn())

    message = "<b>📖 Darslar ro'yxati:</b>"
    message = update.message.reply_text(message, parse_mode="HTML", reply_markup=inlines.get_lessons(lessons))
    context.user_data["last_message_id"] = message.message_id
    return states.TEACHER_GET_LESSON_FOR_TASK


@get_user
def get_lesson_for_task(update, context, user):
    if update and update.message:
        if update.message.text == "⬅️ Orqaga":
            update.message.reply_text("Bosh menyu\nKerakli bo'limni tanlang.", reply_markup=replies.teacher_main())
            context.bot.delete_message(update.message.chat.id, context.user_data["last_message_id"])
            return states.END

    if update and update.callback_query:
        update.callback_query.answer()
        lesson_id = update.callback_query.data.split("_")[1]
        context.user_data["last_lesson"] = lesson_id
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            update.callback_query.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.teacher_main())
            return states.END
        message = f"<b>📊 Topshiriqlar ro'yxati</b>\n\n<b>📗  Dars:</b> {lesson.title}\n"
        message = update.callback_query.message.reply_text(
            message,
            reply_markup=inlines.get_tasks(lesson.tasks.all()),
            parse_mode="html"
        )
        context.user_data["last_message_id"] = message.message_id
        update.callback_query.delete_message()
        return states.TEACHER_GET_TASK


@get_user
def get_task_students(update, context, user):
    if update and update.message:
        group = Group.objects.get(id=context.user_data["selected_group"])
        lessons = group.finished_lessons.all()
        if update.message.text == "⬅️ Orqaga":
            context.bot.delete_message(update.message.chat.id, context.user_data["last_message_id"])
            message = "<b>📖 Darslar ro'yxati:</b>"
            message = update.message.reply_text(message, parse_mode="HTML", reply_markup=inlines.get_lessons(lessons))
            context.user_data["last_message_id"] = message.message_id
            return states.TEACHER_GET_LESSON_FOR_TASK

    if update and update.callback_query:
        update.callback_query.answer()
        task_id = update.callback_query.data.split("_")[1]
        context.user_data["last_task"] = task_id
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            update.callback_query.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.teacher_main())
            return states.END

        message = f"📖 {task.body}"
        students_tasks = StudentTask.objects.filter(task=task)
        message = update.callback_query.message.reply_text(message, reply_markup=inlines.get_students_task_status(students_tasks))
        context.user_data["last_message_id"] = message.message_id
        update.callback_query.delete_message()
        return states.TEACHER_GET_TASK_DETAILS


@get_user
def get_task_details(update, context, user):
    if update and update.message:
        if update.message.text == "⬅️ Orqaga":
            context.bot.delete_message(update.message.chat.id, context.user_data["last_message_id"])
            lesson_id = context.user_data["last_lesson"]
            try:
                lesson = Lesson.objects.get(id=lesson_id)
            except Lesson.DoesNotExist:
                update.callback_query.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.teacher_main())
                return states.END
            message = f"<b>📊 Topshiriqlar ro'yxati</b>\n\n<b>📗  Dars:</b> {lesson.title}\n"
            message = update.message.reply_text(
                message,
                reply_markup=inlines.get_tasks(lesson.tasks.all()),
                parse_mode="html"
            )
            context.user_data["last_message_id"] = message.message_id
            return states.TEACHER_GET_TASK

    if update and update.callback_query:
        update.callback_query.answer()
        task_id = update.callback_query.data.split("_")[1]
        context.user_data["last_task"] = task_id
        try:
            task = StudentTask.objects.get(id=task_id)
        except StudentTask.DoesNotExist:
            update.callback_query.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.teacher_main())
            return states.END

        message = f"🎓 {task.student.first_name}\n"
        message += f"📖 Topshiriq: {task.task.body}"
        message += f"📝 Javob: {task.body}"

        update.callback_query.message.reply_text(message, reply_markup=inlines.confirm_task(task_id))
        update.callback_query.delete_message()
        return states.TEACHER_CONFIRM_TASK


@get_user
def confirm_task(update, context, user):
    if update and update.message:
        if update.message.text == "⬅️ Orqaga":
            update.message.reply_text("Bosh menyu\nKerakli bo'limni tanlang.", reply_markup=replies.teacher_main())
            return states.END

    if update and update.callback_query:
        update.callback_query.answer()
        task_id = update.callback_query.data.split("_")[1]
        try:
            task = StudentTask.objects.get(id=task_id)
        except StudentTask.DoesNotExist:
            update.callback_query.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.teacher_main())
            return states.END

        task.is_completed = True
        task.save(update_fields=["is_completed"])
        update.callback_query.message.reply_text("Topshiriq tasdiqlandi.", reply_markup=replies.back_btn())
        update.callback_query.delete_message()

        message = f"📖 {task.body}"
        students_tasks = StudentTask.objects.filter(task=task.task)
        message = update.callback_query.message.reply_text(
            message, reply_markup=inlines.get_students_task_status(students_tasks))
        context.user_data["last_message_id"] = message.message_id
        return states.TEACHER_GET_TASK_DETAILS


@get_user
def get_random_student(update, context, user):
    group = context.user_data.get("selected_group")
    group = Group.objects.get(id=group)
    students = group.members.all().order_by("?").first()
    update.message.reply_text(f"📖 {students.first_name} {students.last_name}", reply_markup=replies.teacher_main())
    return states.END