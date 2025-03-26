from aiogram.utils.keyboard import InlineKeyboardBuilder


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
    
    
    