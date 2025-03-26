from aiogram.fsm.state import StatesGroup, State

class Auth(StatesGroup):
    phone_number: str = State()
    verify_code: str = State()
    password: str = State()