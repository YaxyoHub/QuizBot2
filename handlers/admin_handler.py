from aiogram import F, Router
from aiogram.types import Message, Poll
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from loader import bot

from states.states import AdminAddState, BroadcastState, AddQuizState
from keyboard.reply import admin_menu
from database.sql_db import (check_admin, add_admin, get_user_count, 
                             get_users_id, add_quiz)

admin_router = Router()

@admin_router.message(Command('admin'))
async def admin_cmd(message: Message):
    if check_admin(message.from_user.id):
        await message.answer(f"Salom Admin", reply_markup=admin_menu())
        return
    await message.answer("⚠️ <b>Bu buyruq faqat adminlar uchun</b>")

# Admin qo'shish
@admin_router.message(F.text == "➕ Admin qo'shish")
async def add_admin_func(message: Message, state: FSMContext):
    await message.answer("Admin ismini kiriting:")
    await state.set_state(AdminAddState.name)

@admin_router.message(AdminAddState.name)
async def get_admin_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Admin telefon raqamini kiriting: (<i>misol +998942140551</i>)")
    await state.set_state(AdminAddState.phone)

@admin_router.message(AdminAddState.phone)
async def get_admin_phone(message: Message, state: FSMContext):
    phone = message.text.strip()

    if phone.startswith("+998") and phone[1:].isdigit() and len(phone) == 13:
        await state.update_data(phone=phone)
        await message.answer("Admin username'ni kiriting")
        await state.set_state(AdminAddState.username)
        return

    await message.answer(
        "⚠️ <b>Telefon raqam noto'g'ri kiritildi</b>\nIltimos, +998 bilan boshlanuvchi 13 xonali raqam kiriting."
    )

@admin_router.message(AdminAddState.username)
async def get_admin_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Admin idsini kiriting")
    await state.set_state(AdminAddState.user_id)

@admin_router.message(AdminAddState.user_id)
async def get_admin_id(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    data = await state.get_data()
    add_admin(
        data['name'],
        data['phone'],
        data['username'],
        data['user_id']
    )
    await message.answer("Admin bazaga qo'shildi ✅", reply_markup=admin_menu())

# Foydalanuvchilarni ko'rish
@admin_router.message(F.text == "👥 Foydalanuvchilarni ko'rish")
async def see_users(message: Message):
    count = get_user_count()

    await message.answer(f"👥 Botda {count} ta foydalanuvchi bor", reply_markup=admin_menu())

# Xabar yuborish 
@admin_router.message(F.text == "📤 Xabar yuborish")
async def send_message(message: Message, state: FSMContext):
    await message.answer("✏️ Qaysi turdagi xabar yubormoqchisiz? (text, rasm, video, va h.k.)\nIltimos, yuboring:")
    await state.set_state(BroadcastState.content)

@admin_router.message(BroadcastState.content)
async def broadcast_any_message(message: Message, state: FSMContext):
    users = get_users_id()
    count = 0

    for user in users:
        user_id = user[0]
        try:
            if message.text:
                await bot.send_message(user_id, message.text)
            elif message.photo:
                await bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                await bot.send_video(user_id, message.video.file_id, caption=message.caption)
            elif message.audio:
                await bot.send_audio(user_id, message.audio.file_id, caption=message.caption)
            elif message.voice:
                await bot.send_voice(user_id, message.voice.file_id, caption=message.caption)
            elif message.document:
                await bot.send_document(user_id, message.document.file_id, caption=message.caption)
            else:
                continue  # noma'lum turdagi xabar bo‘lsa, yubormaydi

            count += 1

        except Exception as e:
            print(f"Xatolik {user_id} uchun: {e}")

    await message.answer(f"✅ Xabar {count} ta foydalanuvchiga yuborildi.")
    await state.clear()

# Quiz qabul qilish

@admin_router.message(F.text == "➕ Savol qo'shish")
async def ask_quiz(message: Message, state: FSMContext):
    await message.answer("📩 Iltimos, test (quiz) yuboring.\n❗️Faqat *Quiz* turidagi Poll yuboring.")
    await state.set_state(AddQuizState.waiting_for_poll)


@admin_router.message(AddQuizState.waiting_for_poll)
async def save_quiz(message: Message, state: FSMContext):
    if not message.poll or message.poll.type != "quiz":
        await message.answer("⚠️ Iltimos, faqat *quiz* turidagi poll yuboring.")
        return

    poll = message.poll
    question = poll.question
    options = [option.text for option in poll.options]
    correct_option_id = poll.correct_option_id

    add_quiz(question, options, correct_option_id)

    await message.answer("✅ Quiz saqlandi.")
    await state.clear()

