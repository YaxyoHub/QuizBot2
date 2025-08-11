from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    name = State()


    


class AdminAddState(StatesGroup):
    name = State()
    phone = State()
    username = State()
    user_id = State()

class BroadcastState(StatesGroup):
    content = State()

class AddQuizState(StatesGroup):
    waiting_for_poll = State()

