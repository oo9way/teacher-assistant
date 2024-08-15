from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from group.models import Group


def inline_groups(key):
    groups = Group.objects.all()
    keyboard = [
        [
            InlineKeyboardButton(group.name, callback_data=f'{key}_{group.id}')
            for group in groups
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def approve_student(student_id, group_id):
    keyboard = [
        [
            InlineKeyboardButton("✅", callback_data=f'approve_{student_id}_{group_id}'),
            InlineKeyboardButton("❌", callback_data=f'reject_{student_id}_{group_id}')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def uncompleted_tasks(tasks):
    keyboard = []

    for task in tasks:
        keyboard.append(
            [
                InlineKeyboardButton(task.task.body[:100], callback_data=f'task_{task.id}')
            ]
        )

    return InlineKeyboardMarkup(keyboard)


def uncompleted_questions(questions):
    keyboard = []

    for question in questions:
        keyboard.append(
            [
                InlineKeyboardButton(question.title, callback_data=f'question_{question.id}')
            ]
        )

    return InlineKeyboardMarkup(keyboard)


def get_lessons(lessons):
    keyboard = []

    for lesson in lessons:
        keyboard.append(
            [
                InlineKeyboardButton(lesson.title, callback_data=f'lesson_{lesson.id}')
            ]
        )

    return InlineKeyboardMarkup(keyboard)


def get_tasks(tasks):
    keyboard = []

    for task in tasks:
        keyboard.append(
            [
                InlineKeyboardButton(task.body[:100], callback_data=f'task_{task.id}')
            ]
        )

    return InlineKeyboardMarkup(keyboard)


def get_students_task_status(student_tasks):
    keyboard = []

    for student_task in student_tasks:
        sign = "✅" if student_task.is_completed else "❌"
        keyboard.append(
            [
                InlineKeyboardButton(f"{student_task.student.first_name} {sign}", callback_data=f'studenttask_{student_task.id}')
            ]
        )

    return InlineKeyboardMarkup(keyboard)


def confirm_task(student_task_id):
    keyboard = [
        [
            InlineKeyboardButton("✅", callback_data=f'confirmtask_{student_task_id}'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)