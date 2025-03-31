from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.bot.fsm import DeletePublic
from src.bot.keyboards import menu_keyboard
from src.bot.global_classes import collector
from src.logger import bot_logger
from src.bot.global_classes import bot


delete_router = Router()

try:
    @delete_router.callback_query(F.data == 'delete_pub')
    async def delete_handler(callback: CallbackQuery, state: FSMContext):
        if len(collector.publics):
            await callback.message.answer('Введите индивидуальный id паблика для удаления.')
            await callback.message.answer('Если хотите выйти введите "cancel".')
            await callback.answer()
            
            await state.set_state(DeletePublic.id)
        else:
            await callback.answer('Нет пабликов, значит нечего удалять')

    @delete_router.message(DeletePublic.id, F.text == 'cancel')
    async def cancel_del_handler(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(text='Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())

    @delete_router.message(DeletePublic.id)
    async def catch_id_del_handler(message: Message, state: FSMContext):
        try:
            if message.text.isdigit():
                if not collector.get_public(message.text).started:
                    collector.delete_public(message.text)
                    
                    await message.answer('Паблик был успешно удален!')
                    await state.clear()
                    await message.answer(text='Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
                else:
                    await message.answer('Этот паблик находится в работе. Удалите его когда он будет остановлен.')
                    await message.answer(text='Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
            else:
                await message.answer('Вы не правильно ввели id, попробуйте еще раз.')
                
        except KeyError:
            await message.answer('Вы не правильно ввели id, попробуйте еще раз.')
            
        except Exception as ex:
            bot_logger.error(f'Произошла ошибка: {ex}')
            state.clear()
            await message.answer('Произошла неожиданная ошибка, попробуйте позже.')
            await message.answer(text='Приветствую. Выбери свои первые действия.', reply_markup=menu_keyboard())
            
except Exception as ex:
    bot_logger.error(f'Произошла ошибка: {ex}')
    bot.send_message(1162899410, f'Произошла ошибка: {ex}')
