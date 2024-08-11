from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from group.models import Group


def inline_groups():
    groups = Group.objects.all()
    keyboard = [
        [
            InlineKeyboardButton(group.name, callback_data=f'rtj_{group.id}')
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
