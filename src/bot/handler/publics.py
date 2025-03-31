from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import os

from src.bot.global_classes import collector
from src.bot.utils import create_str_public_list
from src.bot.keyboards import publics_keyboard, menu_keyboard
from src.settings import Settings
from src.bot.fsm import AddPublic
from src import objects
from src.logger import bot_logger
from src.bot.global_classes import bot
from src.my_exceptions import PublicsLenException, NoValidIdException


publics_router = Router()
settings = Settings()

try:
    @publics_router.callback_query(F.data == 'publics')
    async def publics_handler(callback: CallbackQuery):
        if len(os.listdir(f'.{settings.SLESH}{settings.CREDS_PATH}')):
            if len(collector.publics):
                text = create_str_public_list()
            else:
                text = 'Здесь будут отображаться ваши будущие паблики.'
                
            await callback.message.edit_text(text=text, reply_markup=publics_keyboard())
        else:
            await callback.answer('Cначала пройдите авторизацию')
            
    @publics_router.callback_query(F.data == 'back')
    async def back_handler(callback: CallbackQuery):
        await callback.message.edit_text(text='Приветствую. Выбери свои первые действия.', 
                                        reply_markup=menu_keyboard())

    @publics_router.callback_query(F.data == 'add_pub')
    async def add_handler(callback: CallbackQuery, state: FSMContext):
        await state.set_state(AddPublic.public_id)
        await callback.message.answer('Введите id своего паблика, согласно инструкции.')
        await callback.message.answer('Если хотите выйти, введите "cancel".')
        await callback.answer()

    @publics_router.message(AddPublic.public_id, F.text == 'cancel')
    async def cancel_pub_handler(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(text='Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())

    @publics_router.message(AddPublic.public_id)
    async def catch_public_id_handler(message: Message, state: FSMContext):
        await state.update_data(public_id=message.text)
        await state.set_state(AddPublic.inter_public_id)
        
        await message.answer('Теперь введите id паблика для отслеживания.')

    @publics_router.message(AddPublic.inter_public_id)
    async def catch_inter_public_id_handler(message: Message, state: FSMContext):
        if message.text[0] == '-' and message.text[1:].isdigit():
            await state.update_data(inter_public_id=message.text)
            await state.set_state(AddPublic.interval)
            
            await message.answer('Введите интервал публикования видео, в минутах.')
        else:
            await message.answer('Вы не правильно ввели отслеживаемый паблик, попробуйте еще раз.')

    @publics_router.message(AddPublic.interval)
    async def catch_interval_handler(message: Message, state: FSMContext):
        if message.text.isdigit():
            await state.update_data(interval=int(message.text))
            await state.set_state(AddPublic.id)
            
            await message.answer('Введите индивидуальный id паблика.')
        else:
            await message.answer('Вы не правильно ввели интервал, попробуйте еще раз.')

    @publics_router.message(AddPublic.id)
    async def catch_id_handler(message: Message, state: FSMContext):
        try:
            if message.text.isdigit():
                data = await state.get_data()
                
                collector.add_public(objects.Public(data['public_id'], objects.Interceptor(data['inter_public_id']), 
                                    objects.VideoQueue(data['interval'])), message.text)
                    
                await state.clear()    
                collector.save_state()

                objects.UserAuthorizer().refresh_anonym_token()
                
                await message.answer('Паблик успешно добавлен!')
                await message.answer(text='Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
            else:
                await message.answer('Вы не правильно ввели id, попробуйте еще раз.')
                
        except NoValidIdException:
            await message.answer('Вы ввели уже существующий id, попробуйте снова.')
            
        except PublicsLenException:
            await state.clear()
            await message.answer('Достигнуто максимальное количество пабликов.')
            await message.answer(text='Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
            
        except Exception:
            await state.clear()
            await message.answer('Произошла неожиданная ошибка, попробуйте позже.')
            await message.answer(text='Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
            
except Exception as ex:
    bot_logger.error(f'Произошла ошибка: {ex}')
    bot.send_message(1162899410, f'Произошла ошибка: {ex}')