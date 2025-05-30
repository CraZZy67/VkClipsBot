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

class DeletePublic(StatesGroup):
    id: str = State()

class ChangeInter(StatesGroup):
    id: str = State()
    id_data: str = None

class AddVideo(StatesGroup):
    id: str = State()
    id_data: str = None

class ChangeInterval(StatesGroup):
    interval: str = State()
    id_data: str = None