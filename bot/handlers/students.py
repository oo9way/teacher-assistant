from bot.decorator import get_user
from telegram import ReplyKeyboardRemove
from bot.keyboards import replies, inlines
from student.models import StudentTask, StudentAnswer
from course.models import Lesson, QuestionSet, Question
from bot import states


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

    if update.message and update.message.text == "⬅️ Orqaga":
        update.message.reply_text("Bosh menyu\nKerakli bo'limni tanlang.", reply_markup=replies.student_main())
        return states.END

    if not student_tasks:
        message = "✅ Sizda bajarilmagan topshiriqlar mavjud emas. "
        update.message.reply_text(message, reply_markup=replies.student_main())
        return None

    title = "<b>📖 Bajarilmagan topshiriqlar:</b>\n\n"
    update.message.reply_text(title, parse_mode="HTML", reply_markup=replies.back_btn())
    message = ""
    counter = 1
    for task in student_tasks:
        message += f"{counter}. {task.task.body[:100]}\n"
        counter += 1

    update.message.reply_text(message, parse_mode="HTML", reply_markup=inlines.uncompleted_tasks(student_tasks))
    return states.GET_TASK


@get_user
def get_task(update, context, user):
    if update.message and update.message.text == "⬅️ Orqaga":
        update.message.reply_text("Bosh menyu\nKerakli bo'limni tanlang.", reply_markup=replies.student_main())
        return states.END

    if update and not update.callback_query:
        message = "Iltimos, topshiriqni tanlash uchun topshiriq tugmasini bosing."
        student_tasks = StudentTask.objects.filter(student=user, is_completed=False)
        if not student_tasks:
            message = "Sizda bajarilmagan topshiriqlar mavjud emas. "

        update.message.reply_text(message, reply_markup=replies.back_btn())
        return states.GET_TASK

    update.callback_query.answer()

    student_task = update.callback_query.data.split("_")[1]
    context.user_data["last_task"] = student_task

    student_task = StudentTask.objects.get(id=student_task)
    task = student_task.task

    update.callback_query.edit_message_text(f"📖 {task.body}", parse_mode="HTML")
    update.callback_query.message.reply_text(
        "Topshiriqni yakunlash uchun javobingiz havolasini yuboring.",
        reply_markup=replies.back_btn()
    )
    return states.GET_TASK_ANSWER


@get_user
def get_task_answer(update, context, user):
    if update and not update.message:
        message = "Iltimos, topshiriqni yakunlash uchun havola yuboring yoki ortga qayting."
        update.message.reply_text(message, reply_markup=replies.back_btn())
        return states.GET_TASK_ANSWER

    if update.message.text == "⬅️ Orqaga":
        update.message.text = ""
        return get_uncompleted_tasks(update, context)

    if not str(update.message.text).startswith("https://"):
        message = "Iltimos, topshiriqni yakunlash uchun faqat havola yuboring."
        update.message.reply_text(message, reply_markup=replies.back_btn())
        return states.GET_TASK_ANSWER

    student_task = StudentTask.objects.get(id=context.user_data["last_task"])
    student_task.body = update.message.text
    student_task.is_completed = True
    student_task.save(update_fields=["body", "is_completed"])

    update.message.reply_text("✅ Topshiriq qabul qilindi. ", reply_markup=replies.student_main())
    return states.END


@get_user
def get_question_set(update, context, user):
    group = user.groups.all()
    question_sets = []
    for group in group:
        for lesson in group.finished_lessons.all():
            for question_set in lesson.questions.exclude(answered_students=user):
                question_sets.append(question_set)

    if not question_sets:
        update.message.reply_text("✅ Sizda javob berilmagan savollar mavjud emas", reply_markup=replies.student_main())
        return states.END

    message = ""
    counter = 1
    for question_set in question_sets:
        message += f"{counter}. {question_set.title}\n"
        counter += 1
    update.message.reply_text("📖 Javob berilmagan savollar to'plami", reply_markup=replies.back_btn())
    update.message.reply_text(message, parse_mode="HTML", reply_markup=inlines.uncompleted_questions(question_sets))
    return states.QUESTION_SINGLE


@get_user
def question_single(update, context, user):
    if update and update.message:
        if update.message.text == "⬅️ Orqaga":
            update.message.reply_text("Bosh menyu\nKerakli bo'limni tanlang.", reply_markup=replies.student_main())
            return states.END

    if update and update.callback_query:
        update.callback_query.answer()
        question_set = update.callback_query.data.split("_")[1]
        context.user_data["last_question_set"] = question_set
        try:
            question_set = QuestionSet.objects.get(id=question_set)
        except QuestionSet.DoesNotExist:
            update.callback_query.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.student_main())
            return states.END

        update.callback_query.message.reply_text(
            f"📖 {question_set.title}\n\nSavollarni boshlashga tayyormisiz ?.\n"
            "<i>Eslatma savollar boshlanganda barcha savollarga javob berish shart!!!</i>",
            reply_markup=replies.yes_or_no(),
            parse_mode="html"
        )
        return states.QUESTION_NOTIFY

    return get_question_set(update, context)


@get_user
def notify_question_start(update, context, user):
    text = update.message.text
    if text == "✅ Ha":
        question_set = context.user_data["last_question_set"]
        try:
            question_set = QuestionSet.objects.get(id=question_set)
        except QuestionSet.DoesNotExist:
            update.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.student_main())
            return states.END

        questions = question_set.questions.all()
        for question in questions:
            if not StudentAnswer.objects.filter(student=user, question=question).exists():
                update.message.reply_text(f"📖 {question.title}", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
                context.user_data["last_question"] = question.id
                return states.GET_ANSWER

        update.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.student_main())
        return states.END

    if text == "❌ Yo'q":
        update.message.reply_text("Bosh sahifa \nKerakli bo'limni tanlang", reply_markup=replies.student_main())
        return states.END


@get_user
def get_answer(update, context, user):
    text = update.message.text
    try:
        question_set = QuestionSet.objects.get(id=context.user_data["last_question_set"])
    except QuestionSet.DoesNotExist:
        update.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.student_main())
        return states.END

    try:
        question = Question.objects.get(id=context.user_data["last_question"])
    except Question.DoesNotExist:
        update.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.student_main())
        return states.END

    StudentAnswer.objects.update_or_create(student=user, question=question, defaults={"body": text})

    for question in question_set.questions.all():
        if not StudentAnswer.objects.filter(student=user, question=question).exists():
            update.message.reply_text(f"📖 {question.title}", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
            context.user_data["last_question"] = question.id
            return states.GET_ANSWER

    update.message.reply_text("✅ Siz barcha savollarga javob berdingiz.", reply_markup=replies.student_main())
    question_set.answered_students.add(user)
    question_set.save(update_fields=["answered_students"])
    return states.END


@get_user
def get_results(update, context, user):
    question_sets = QuestionSet.objects.filter(answered_students=user)
    if not question_sets:
        update.message.reply_text("Sizda hozircha hech qanday natijalar mavjud emas",
                                  reply_markup=replies.student_main())
        return states.END

    message = ""
    counter = 1
    for question_set in question_sets:
        message += f"{counter}. {question_set.title}\n"
        counter += 1
    update.message.reply_text("📖 Natijalarni ko'rish uchun savol to'plamini tanlang.", reply_markup=replies.back_btn())
    update.message.reply_text(message, parse_mode="HTML", reply_markup=inlines.uncompleted_questions(question_sets))
    return states.GET_RESULT_DETAILS


@get_user
def get_result_details(update, context, user):
    if update and update.message:
        if update.message.text == "⬅️ Orqaga":
            update.message.reply_text("Bosh menyu\nKerakli bo'limni tanlang.", reply_markup=replies.student_main())
            return states.END
    if update and update.callback_query:
        update.callback_query.answer()
        question_set = update.callback_query.data.split("_")[1]
        try:
            question_set = QuestionSet.objects.get(id=question_set)
        except QuestionSet.DoesNotExist:
            update.callback_query.message.reply_text("Noto'g'ri so'rov", reply_markup=replies.student_main())
            return states.END

        message = f"📝️️️️️️ Natija: {question_set.title}\n\n"
        wrong = 0
        correct = 0
        unchecked = 0
        answers = StudentAnswer.objects.filter(student=user, question__question_set=question_set)
        for answer in answers:
            if answer.is_correct and answer.is_checked:
                correct += 1

            if not answer.is_correct and answer.is_checked:
                wrong += 1

            if not answer.is_checked and not answer.is_correct:
                unchecked += 1

        message += f"<b>✅ To'g'ri javoblar:</b> {correct}\n"
        message += f"<b>❌ Noto'g'ri javoblar:</b> {wrong}\n"
        message += f"<b>🔘 Tekshirilmagan javoblar:</b> {unchecked}\n"

        update.callback_query.message.reply_text(message, parse_mode="HTML", reply_markup=replies.student_main())
        return states.END
