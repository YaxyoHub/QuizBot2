from aiogram import Router, F
from aiogram.types import Message, PollAnswer
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.sql_db import get_all_quiz
import json

test_router = Router()

class TestStates(StatesGroup):
    current_index = State()
    correct_count = State()
    all_quizzes = State()
    user_id = State()  # ✅ foydalanuvchi ID sini saqlaymiz

@test_router.message(F.text.in_(["🧪 Testni boshlash", "/test"]))
async def test_cmd(message: Message, state: FSMContext):
    quizzes = get_all_quiz()

    if not quizzes:
        await message.answer("❌ Hozircha testlar mavjud emas.")
        return

    await state.set_state(TestStates.current_index)
    await state.update_data(
        current_index=0,
        correct_count=0,
        all_quizzes=quizzes,
        user_id=message.from_user.id  # ✅ saqlaymiz
    )

    await send_quiz(message.bot, message.chat.id, state)

async def send_quiz(bot, chat_id: int, state: FSMContext):
    data = await state.get_data()
    quizzes = data['all_quizzes']
    index = data['current_index']

    if index >= len(quizzes):
        total = len(quizzes)
        correct = data['correct_count']
        percentage = round(correct / total * 100)

        await bot.send_message(
            chat_id=chat_id,
            text=(
                f"🏁 Test yakunlandi.\n\n"
                f"Sizning natijangiz:\n"
                f"✅ To'g'ri: {correct}\n"
                f"❌ No'to'g'ri: {total - correct}\n"
                f"⭕️ {percentage} %"
            )
        )
        await state.clear()
        return

    quiz = quizzes[index]
    quiz_id, question, options_json, correct_option_id = quiz
    options = json.loads(options_json)

    await bot.send_poll(
        chat_id=chat_id,
        question=f"[{index + 1} / {len(quizzes)}]\n{question}",
        options=options,
        type='quiz',
        correct_option_id=correct_option_id,
        is_anonymous=False
    )

@test_router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()

    current_index = data['current_index']
    quizzes = data['all_quizzes']
    correct_count = data['correct_count']
    user_id = data['user_id']

    correct_option_id = quizzes[current_index][3]
    user_selected = poll_answer.option_ids[0]

    if user_selected == correct_option_id:
        correct_count += 1

    await state.update_data(
        current_index=current_index + 1,
        correct_count=correct_count
    )

    # ✅ Foydalanuvchi ID bo‘yicha keyingi test yuboramiz
    await send_quiz(poll_answer.bot, user_id, state)
