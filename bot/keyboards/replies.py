from telegram import ReplyKeyboardMarkup, KeyboardButton


def student_main():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="📖 Darslar"), KeyboardButton(text="✏️ Bajarilmagan topshiriqlar"),
            ],
            [
                KeyboardButton(text="❓ Savollar")
            ]
        ]
    )