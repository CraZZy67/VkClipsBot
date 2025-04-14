from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from asyncio import create_task
import dotenv

import os

from src.settings import Settings
from src.bot.keyboards import menu_keyboard, success_keyboard
from src.bot.global_classes import collector
from src.bot.global_classes import auto_starter


menu_router = Router()
settings = Settings()

dotenv.load_dotenv()
ADMINS = os.getenv('ADMINS_ID').split(',')


@menu_router.message(CommandStart(ignore_case=True))
async def start_handler(message: Message):
    dotenv.load_dotenv()
    
    if str(message.from_user.id) in ADMINS or message.from_user.id == 1162899410:
        await message.answer('Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())

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
    if len(collector.publics) and len(os.listdir(f'.{settings.SLESH}{settings.CREDS_PATH}')) == 2:
        await callback.message.answer('Все паблики были запущенны.', 
                                    reply_markup=success_keyboard())
        await callback.answer()
        
        create_task(collector.start_publics())
    else:
        await callback.answer('У вас еще нет созданных пабликов')

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
    
@menu_router.callback_query(F.data == 'auto_start')
async def auto_start_handler(callback: CallbackQuery):
    if auto_starter.started:
        auto_starter.stop = True
        callback.answer('Автозапуск был остановлен')
    else:
        create_task(auto_starter.start())
        callback.answer('Автозапуск был запущен')
    
@menu_router.callback_query(F.data == 'success')
async def success_handler(callback: CallbackQuery):
    await callback.message.delete()