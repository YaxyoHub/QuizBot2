from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.sql_db import get_all_quiz, delete_quiz

delete_router = Router()

@delete_router.message(F.text == "🗑 Savolni o‘chirish")
async def show_quizzes_for_delete(message: types.Message):
    quizzes = get_all_quiz()

    if not quizzes:
        await message.answer("❌ Hech qanday test mavjud emas.")
        return

    for quiz in quizzes:
        quiz_id, question, *_ = quiz
        short_question = question[:50] + "..." if len(question) > 50 else question

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ O‘chirish", callback_data=f"delete_{quiz_id}")]
        ])

        await message.answer(f"📝 {short_question}", reply_markup=markup)

@delete_router.callback_query(F.data.startswith("delete_"))
async def delete_quiz_callback(callback: CallbackQuery):
    quiz_id = int(callback.data.split("_")[1])
    delete_quiz(quiz_id)
    await callback.message.edit_text("✅ Savol o‘chirildi.")
    await callback.answer("O‘chirildi!")
