from aiogram import Router, F
from aiogram.types import Message

error_router = Router()

@error_router.message(F.text)
async def error_cmd(message: Message):
    await message.reply(f"⚠️ <i>Iltimos botga to'g'ridan-to'g'ri xabar yubormang</i>")