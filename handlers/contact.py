from aiogram import Router, F
from aiogram.types import Message
from database.sql_db import get_admin

contact_router = Router()

@contact_router.message(F.text == "📞 Admin bilan bog‘lanish")
async def contact_admins(message: Message):
    admins = get_admin()
    if not admins:
        await message.answer("Hozircha adminlar mavjud emas.")
        return

    text = "📋 Adminlar ro'yxati:\n\n"
    for i, admin in enumerate(admins, start=1):
        _, name, phone, username, _ = admin
        text += (
            f"▪️ Admin {i}:\n"
            f"👤 Ism: {name}\n"
            f"📞 Telefon: {phone}\n"
            f"🇺🇿 Telegram: @{username}\n\n"
        )

    await message.answer(text)
