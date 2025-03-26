from aiogram.fsm.state import StatesGroup, State

class Auth(StatesGroup):
    phone_number: str = State()
    verify_code: str = State()
    password: str = State()

class AddPublic(StatesGroup):
    public_id: str = State()
    inter_public_id: str = State()
    interval: int = State()
    id: str = State()