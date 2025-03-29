from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import re

from src.bot.fsm import Auth
from src.settings import Settings
from src.bot.keyboards import menu_keyboard
from src.objects.authorizer import UserAuthorizer
from src.logger import bot_logger


auth_router = Router()
authorizer = None

try:
    @auth_router.callback_query(F.data == 'auth')
    async def auth_handler(callback: CallbackQuery, state: FSMContext):
        await state.set_state(Auth.phone_number)
        
        global authorizer
        
        authorizer = UserAuthorizer()
        
        await callback.message.answer('Введите номер своего телефона без кода страны.')
        await callback.message.answer('Если вы случайно сюда попали то напишите "cancel", позже у вас не получится выйти!')
        await callback.answer()

    @auth_router.message(Auth.phone_number, F.text == "cancel")
    async def cancel_handler(message: Message, state: FSMContext):
        await state.clear()
        await message.answer('Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())

    @auth_router.message(Auth.phone_number)
    async def catch_phone_number_handler(message: Message, state: FSMContext):
        if bool(re.match(r'^\d{10}$', message.text)):
            try:
                authorizer.send_verify_code(message.text)
            except Exception as ex:
                await state.clear()
                authorizer.driver.quit()
                
                bot_logger.error('Ошибка функции отправки кода верификации: {ex}')
                await message.answer('Произошла неожиданная ошибка, попробуйте перезапустить авторизацию.')
                await message.answer('Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
                return None
                
            await message.answer('К вам на телефон был отправлен код, введите его.')
            await message.answer('Если код не придет в течении пары минут, введите "retry".')
            await state.set_state(Auth.verify_code)
        else:
            await message.answer('Вы ввели не правильный номер телефона, повторите попытку.')

    @auth_router.message(Auth.verify_code, F.text == "retry")
    async def retry_handler(message: Message, state: FSMContext):
        await state.clear()
        authorizer.driver.quit()
        
        await message.answer('Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())

    @auth_router.message(Auth.verify_code)
    async def catch_verify_code_handler(message: Message, state: FSMContext):
        if bool(re.match(r'^\d{6}$', message.text)):
            try:
                authorizer.enter_verify_code(message.text)
            except Exception as ex:
                await state.clear()
                authorizer.driver.quit()
                
                bot_logger.error('Ошибка функции ввода кода верификации: {ex}')
                await message.answer('Произошла ошибка, попробуйте перезапустить авторизацию. Внимательней введите данные.')
                await message.answer('Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
                return None
            
            await message.answer('Теперь введите пароль.')
            await state.set_state(Auth.password)
        else:
            await message.answer('Вы ввели не правильный код, попробуйте еще раз.')
            
    @auth_router.message(Auth.password)
    async def catch_password_handler(message: Message, state: FSMContext):
        try:
            authorizer.enter_password(message.text)
            authorizer.save_session_creds()
        except Exception as ex:
            await state.clear()
            authorizer.driver.quit()
            
            bot_logger.error('Ошибка функции ввода пароля: {ex}')
            await message.answer('Произошла ошибка, попробуйте перезапустить авторизацию. Внимательней введите данные.')
            await message.answer('Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
            return None
            
        await state.clear()
        await message.answer('Поздравляю! Авторизация прошла успешно.')
        await message.answer('Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
        
except Exception as ex:
    bot_logger.error('Произошла ошибка: {ex}')
    authorizer.driver.quit()