from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup([
        [
            KeyboardButton("Маҳсулотлар 🛒")
        ],
        [
            KeyboardButton("🎁 Акция"), KeyboardButton("📞 Контактлар")
        ],
        [
            KeyboardButton("📦 Буюртмаларим"), KeyboardButton("🤝 Қоидалар")
        ],
        [
            KeyboardButton("📌 Биз ҳақимизда"), KeyboardButton("📃 Cертификат")
        ],
        [
            KeyboardButton("🌐 Ижтимоий тармоқлар")
        ]
    ], resize_keyboard=True)