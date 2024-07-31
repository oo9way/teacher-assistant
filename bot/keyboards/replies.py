from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup([
        [
            KeyboardButton("Buyurtma berish"), KeyboardButton("Savat")
        ],
        [
            KeyboardButton("Buyurtma holatini tekshirish")
        ]
    ], resize_keyboard=True)