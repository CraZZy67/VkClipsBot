from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.global_classes import collector
from src.bot.collback_factory import PublicsFactory


def menu_keyboard():
    builder = InlineKeyboardBuilder()
    
    builder.button(text='Паблики', callback_data='publics')
    builder.button(text='Авторизация', callback_data='auth')
    builder.button(text='Инструкция', callback_data='instruction')
    builder.button(text='Остановить все паблики', callback_data='stop_all')
    builder.button(text='Запустить все паблики', callback_data='start_all')
    builder.button(text='Сохранить состояние', callback_data='save_state')
    
    builder.adjust(3, 2, 1)
    return builder.as_markup()

def success_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Понятно', callback_data='success')
    return builder.as_markup()
    
def publics_keyboard():
    builder = InlineKeyboardBuilder()
    
    for k, v in collector.publics.items():
        builder.button(text=f'Public {k} - {v.public_id}', 
                       callback_data=PublicsFactory(id=k, info='public'))
    
    builder.button(text='Добавить паблик', callback_data='add_pub')
    builder.button(text='Удалить паблик', callback_data='delete_pub')
    builder.button(text='Назад', callback_data='back')
    
    builder.adjust(2, repeat=True)
    return builder.as_markup()

def current_keyboard(public_id: str):
    builder = InlineKeyboardBuilder()
    
    builder.button(text='Старт', callback_data=PublicsFactory(id=public_id, info='start'))
    builder.button(text='Стоп', callback_data=PublicsFactory(id=public_id, info='stop'))
    builder.button(text='Видео очередь', callback_data=PublicsFactory(id=public_id, info='video_queue'))
    builder.button(text='Изменить паблик для отслеживания', callback_data=PublicsFactory(id=public_id, info='change_inter_public'))
    builder.button(text='Назад', callback_data='back')
    
    builder.adjust(3, 1, 1)
    
    return builder.as_markup()
    