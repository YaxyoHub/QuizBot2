import logging
import asyncio
from aiogram.types import BotCommand

from database import sql_db

from handlers.start_handler import start_router
from handlers.admin_handler import admin_router
from handlers.contact import contact_router
from handlers.test_handler import test_router
from handlers.delete_quiz import delete_router
from handlers.error_handler import error_router

from loader import dp, bot

from middlewares import ThrottlingMiddleware 

dp.message.middleware(ThrottlingMiddleware(limit=1))


dp.include_router(start_router)
dp.include_router(admin_router)
dp.include_router(contact_router)
dp.include_router(test_router)
dp.include_router(delete_router)

dp.include_router(error_router)

async def main():
    # Bazani yaratish
    sql_db.create_db()

    # Bot komandalar
    await bot.set_my_commands([
        BotCommand(command="start", description="Botni ishga tushurish"),
        BotCommand(command='test', description="Testni boshlash uchun"),
        BotCommand(command='about', description="Biz haqimizda"),
        BotCommand(command="admin", description="Admin panel (faqat adminlar uchun)")
    ])

    # Bot ishga tushishi
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
