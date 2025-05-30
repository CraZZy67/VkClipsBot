from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import dotenv

import os
from asyncio import create_task

from src.bot.collback_factory import PublicsFactory
from src.bot.utils import create_public_info, create_queue_info
from src.bot.keyboards import current_keyboard, queue_keyboard
from src.bot.global_classes import collector
from src.logger import bot_logger
from src.bot.fsm import ChangeInter
from src.bot.global_classes import bot
import src.my_exceptions as my_exceptions


current_router = Router()

dotenv.load_dotenv()
ADMINS = os.getenv('ADMINS_ID').split(',')

try:
    @current_router.callback_query(PublicsFactory.filter(F.info == 'public'))
    async def current_handler(callback: CallbackQuery, callback_data: PublicsFactory):
        await callback.message.edit_text(text=create_public_info(collector.get_public(callback_data.id)),
                                        reply_markup=current_keyboard(callback_data.id))

    @current_router.callback_query(PublicsFactory.filter(F.info.in_(['start', 'stop'])))
    async def start_stop_handler(callback: CallbackQuery, callback_data: PublicsFactory):
        if callback_data.info == 'start':
            await callback.answer('Паблик запущен')
            
            public = collector.get_public(callback_data.id)
            
            create_task(public.start())
        else:
            collector.get_public(callback_data.id).stop = True
            await callback.answer('Паблик остановлен')

    @current_router.callback_query(PublicsFactory.filter(F.info == 'change_inter_public'))
    async def change_inter_handler(callback: CallbackQuery, callback_data: PublicsFactory, state: FSMContext):
        if not collector.get_public(callback_data.id).started:
            await state.set_state(ChangeInter.id)
            ChangeInter.id_data = callback_data.id

            await callback.message.answer('Введите id того паблика на который выхотите сменить старый id.')
            await callback.message.answer('Если хотите выйти, введите "cancel".')
            await callback.answer()
        else:
            await callback.answer('Этот паблик находиться в работе.')
            
    @current_router.message(ChangeInter.id, F.text == 'cancel')
    async def cancel_pub_handler(message: Message, state: FSMContext):
        await state.clear()
        
        await message.answer(text=create_public_info(collector.get_public(ChangeInter.id_data)),
                            reply_markup=current_keyboard(ChangeInter.id_data))

    @current_router.message(ChangeInter.id)
    async def catch_id_cur_handler(message: Message, state: FSMContext):
        if message.text[0] == '-' and message.text[1:].isdigit():
            public = collector.get_public(ChangeInter.id_data)
            public.inter_public = message.text
            public.interceptor.inter_public = message.text
            
            public.interceptor.cycles = int()
            public.interceptor.next_hash = str()
            public.interceptor.ids = list()
            
            await state.clear()
            await message.answer('Отслеживаемый паблик был успешно изменен.')
            await message.answer(text=create_public_info(collector.get_public(ChangeInter.id_data)),
                            reply_markup=current_keyboard(ChangeInter.id_data))
        else:
            await message.answer('Вы не правильно ввели отслеживаемый паблик, попробуйте еще раз.')

    @current_router.callback_query(PublicsFactory.filter(F.info == 'video_queue'))
    async def video_queue_handler(callback: CallbackQuery, callback_data: PublicsFactory):
        await callback.message.edit_text(create_queue_info(collector.get_public(callback_data.id)), 
                                        reply_markup=queue_keyboard(callback_data.id))

except my_exceptions.AccessDeniedException as ex:
    bot.send_message(int(ADMINS[0]), f'Произошла ошибка доступа у паблика: {ex.public_id}.')
            
except my_exceptions.NoValidInterPublicException as ex:
    bot.send_message(int(ADMINS[0]), f'У паблика {ex.public_id} был не правильно введен паблик для отслеживания.')
    
except my_exceptions.NoValidOwnPublicException as ex:
    bot.send_message(int(ADMINS[0]), f'У паблика {ex.public_id} был не правильно введен его ID.')
    
except my_exceptions.NoValidVideoPathException as ex:
    bot.send_message(int(ADMINS[0]), f'Ошибка пути у паблика {ex.public_id}. Попробуйте перепроверить его данные.')
    
except Exception as ex:
    bot_logger.error(f'Произошла ошибка: {ex}')
    bot.send_message(1162899410, f'Произошла ошибка: {ex}')