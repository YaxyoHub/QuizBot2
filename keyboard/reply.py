from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧪 Testni boshlash")],
            [KeyboardButton(text="📞 Admin bilan bog‘lanish")]
        ],
        resize_keyboard=True
    )

def end_test_button():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛑 Testni yakunlash")]
        ],
        resize_keyboard=True
    )


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Admin qo'shish")],
            [KeyboardButton(text="👥 Foydalanuvchilarni ko'rish"), KeyboardButton(text="📤 Xabar yuborish")],
            [KeyboardButton(text="🗑 Savolni o‘chirish"), KeyboardButton(text="➕ Savol qo'shish")]
        ],
        resize_keyboard=True
    )

