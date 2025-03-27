from aiogram.filters.callback_data import CallbackData


class PublicsFactory(CallbackData, prefix='pub'):
    id: str
    info: str