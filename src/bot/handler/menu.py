from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from asyncio import create_task
import dotenv

import os

from src.settings import Settings
from src.bot.keyboards import menu_keyboard, success_keyboard
from src.bot.global_classes import collector
from src.logger import bot_logger
from src.my_exceptions import (AccessDeniedException, NoValidInterPublicException,
                               NoValidOwnPublicException, NoValidVideoPathException)


menu_router = Router()
settings = Settings()

@menu_router.message(CommandStart(ignore_case=True))
async def start_handler(message: Message):
    dotenv.load_dotenv()
    
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(settings.START_TXT, reply_markup=menu_keyboard())

@menu_router.callback_query(F.data == 'stop_all')
async def stop_handler(callback: CallbackQuery):
    if len(collector.publics):
        collector.stop_publics()
        await callback.message.answer('Все паблики были остановленны.', 
                                      reply_markup=success_keyboard())
        await callback.answer()
    else:
        await callback.answer('У вас еще нет созданных пабликов')
        await callback.answer()

@menu_router.callback_query(F.data == 'start_all')
async def start_pablics_handler(callback: CallbackQuery):
    try:
        if len(collector.publics) and len(os.listdir(f'./{settings.CREDS_PATH}')) == 2:
            create_task(collector.start_publics())
            
            await callback.message.answer('Все паблики были запущенны.', 
                                        reply_markup=success_keyboard())
            await callback.answer()
        else:
            await callback.answer('У вас еще нет созданных пабликов')
            
    except AccessDeniedException as ex:
        await callback.message.answer(f'Произошла ошибка доступа у паблика: {ex.public_id}.')
        
    except NoValidInterPublicException as ex:
        await callback.message.answer(f'У паблика {ex.public_id} был не правильно введен паблик для отслеживания.')
        
    except NoValidOwnPublicException as ex:
        await callback.message.answer(f'У паблика {ex.public_id} был не правильно введен его ID.')
        
    except NoValidVideoPathException as ex:
        await callback.message.answer(f'Ошибка пути у паблика {ex.public_id}. Попробуйте перепроверить его данные.')
        
    except Exception as ex:
        bot_logger.error(f'Произошла ошибка: {ex}')
        await callback.answer()
        await callback.message.answer('Произошла неожиданная ошибка, попробуйте позже.')


@menu_router.callback_query(F.data == 'save_state')
async def save_sate_handler(callback: CallbackQuery):
    collector.save_state()
    await callback.message.answer('Состояние пабликов было сохранено.',
                                  reply_markup=success_keyboard())
    await callback.answer()

@menu_router.callback_query(F.data == 'instruction')
async def instruction_handler(callback: CallbackQuery):
    file = FSInputFile('instruction.docx')
    await callback.message.answer_document(file, caption='Инструкция к проекту.',
                                           reply_markup=success_keyboard())
    await callback.answer()

@menu_router.callback_query(F.data == 'success')
async def success_handler(callback: CallbackQuery):
    await callback.message.delete()