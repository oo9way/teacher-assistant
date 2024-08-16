from telegram import ReplyKeyboardMarkup, KeyboardButton


def student_main():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="📖 Darslar"), KeyboardButton(text="✏️ Bajarilmagan topshiriqlar"),
            ],
            [
                KeyboardButton(text="❓ Savollar"), KeyboardButton(text="🔖 Natijalar")
            ]
        ]
    )


def back_btn():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="⬅️ Orqaga")
            ]
        ],
        resize_keyboard=True
    )


def yes_or_no():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="✅ Ha"),
                KeyboardButton(text="❌ Yo'q")
            ]
        ],
        resize_keyboard=True
    )


def teacher_main():
    return ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="📝️️️️️️ Guruhni o'zgartirish"),
                KeyboardButton(text="📖 Topshiriqlar"),
            ],

            [KeyboardButton(text="🔐 Tasodifiy ishtirokchilarni tanlash"), ]
        ],
        resize_keyboard=True
    )
