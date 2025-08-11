from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from states.states import RegisterState
from database.sql_db import check_user, add_user, get_user
from keyboard.reply import main_menu

start_router = Router()

@start_router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    name = get_user(message.from_user.id)[0]
    if check_user(message.from_user.id):
        await message.answer(f"Salom {name}", reply_markup=main_menu())
        return
    await message.answer(f"Salom {message.from_user.full_name} 👋\n"
                         "Botda ro'yxatdan o'tish uchun ismingizni kiriting")
    await state.set_state(RegisterState.name)

@start_router.message(RegisterState.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    add_user(data['name'], message.from_user.id)
    await message.answer("Siz botdan ro'yxatdan o'tdingiz ✅\n"
                         "Endi botdan foydalanashingiz mumkin", reply_markup=main_menu())
    await state.clear()
    
@start_router.message(Command("about"))
async def about_cmd(message: Message):
    await message.answer("""
Ushbu bot orqali siz IC3 Digital Literacy Certification 
ga oid testlarni yechinshingiz mumkin.
Buning uchun botga /test deb yozing

https://t.me/fozilovblog                       
""")