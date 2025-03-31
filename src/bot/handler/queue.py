from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.bot.collback_factory import PublicsFactory
from src.bot.fsm import AddVideo, ChangeInterval
from src.bot.global_classes import collector
from src.bot.keyboards import queue_keyboard, current_keyboard
from src.bot.utils import create_queue_info, create_public_info
from src.logger import bot_logger
from src.bot.global_classes import bot
import src.my_exceptions as my_exceptions


queue_router = Router()

try:
    @queue_router.callback_query(PublicsFactory.filter(F.info == 'add_video'))
    async def add_video_handler(callback: CallbackQuery, callback_data: PublicsFactory, state: FSMContext):
        await state.set_state(AddVideo.id)
        AddVideo.id_data = callback_data.id
        
        await callback.message.answer('Введите айди видео которое вы хотите добавить.')
        await callback.message.answer('Если захотите выйти то введите "cancel"')
        await callback.message.answer('Внимание! Айди видео должно пренадлежать только текущего отслеживаемому паблику!')
        await callback.answer()

    @queue_router.message(AddVideo.id, F.text == 'cancel')
    async def catch_cancel_video_id_handler(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(create_queue_info(collector.get_public(AddVideo.id_data)), 
                                            reply_markup=queue_keyboard(AddVideo.id_data))

    @queue_router.message(AddVideo.id)
    async def catch_video_id_handler(message: Message, state: FSMContext):
        try:
            if message.text.isdigit():
                collector.get_public(AddVideo.id_data).add_video(message.text)
                
                await state.clear()
                await message.answer('Видео было успешно добавленно в конец очереди.')
                await message.answer(create_queue_info(collector.get_public(AddVideo.id_data)), 
                                        reply_markup=queue_keyboard(AddVideo.id_data))
            else:
                await message.answer('Вы не правильно ввели id video')
                
        except my_exceptions.AccessDeniedException as ex:
            await state.clear()
            await message.answer(f'Произошла ошибка доступа у паблика: {ex.public_id}.')
            await message.answer(create_queue_info(collector.get_public(AddVideo.id_data)), 
                                        reply_markup=queue_keyboard(AddVideo.id_data))
            
        except my_exceptions.NoFoundVideoException as ex:
            await state.clear()
            await message.answer(f'Такое видео было не найденно: {ex.public_id}.')
            await message.answer(create_queue_info(collector.get_public(AddVideo.id_data)), 
                                        reply_markup=queue_keyboard(AddVideo.id_data))
            
        except my_exceptions.QueueLenException as ex:
            await state.clear()
            await message.answer(f'Слишком много видео, удалите одно если хотите добавить еще: {ex.public_id}.')
            await message.answer(create_queue_info(collector.get_public(AddVideo.id_data)), 
                                        reply_markup=queue_keyboard(AddVideo.id_data))
        except Exception as ex:
            await state.clear()
            bot_logger.error(f'Произошла ошибка: {ex}')
            await message.answer('Произошла неожиданная ошибка, попробуйте позже.')

    @queue_router.callback_query(PublicsFactory.filter(F.info == 'change_interval'))
    async def change_interval_handler(callback: CallbackQuery, callback_data: PublicsFactory, state: FSMContext):
        await state.set_state(ChangeInterval.interval)
        ChangeInterval.id_data = callback_data.id
        
        await callback.message.answer('Введите интервал который на который вы хотите поменять старый.')
        await callback.message.answer('Если захотите выйти то введите "cancel"')
        await callback.answer()

    @queue_router.message(ChangeInterval.interval, F.text == 'cancel')
    async def catch_video_id_handler(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(create_queue_info(collector.get_public(AddVideo.id_data)), 
                                        reply_markup=queue_keyboard(AddVideo.id_data))

    @queue_router.message(ChangeInterval.interval)
    async def catch_video_id_handler(message: Message, state: FSMContext):
            if message.text.isdigit():
                collector.get_public(ChangeInterval.id_data).video_queue.interval = int(message.text)
                
                await state.clear()
                await message.answer('Интервал был успешно изменен.')
                await message.answer(create_queue_info(collector.get_public(ChangeInterval.id_data)), 
                                    reply_markup=queue_keyboard(ChangeInterval.id_data))
            else:
                await message.answer('Вы не правильно ввели интервал.')

    @queue_router.callback_query(PublicsFactory.filter(F.info == 'del_video'))
    async def add_video_handler(callback: CallbackQuery, callback_data: PublicsFactory):
        try:
            collector.get_public(callback_data.id).delete_video()
            await callback.answer('Видео было успешно удаленно')
        except my_exceptions.QueueLenException:
            await callback.answer('Осталось слишком мало видео')

    @queue_router.callback_query(PublicsFactory.filter(F.info == 'stop_video'))
    async def add_video_handler(callback: CallbackQuery, callback_data: PublicsFactory):
        collector.get_public(callback_data.id).video_queue.run = False
        await callback.answer('Очередь успешно остановленна')

    @queue_router.callback_query(PublicsFactory.filter(F.info == 'back_pub'))
    async def add_video_handler(callback: CallbackQuery, callback_data: PublicsFactory):
        await callback.message.edit_text(text=create_public_info(collector.get_public(callback_data.id)),
                                        reply_markup=current_keyboard(callback_data.id))

except Exception as ex:
    bot_logger.error(f'Произошла ошибка: {ex}')
    bot.send_message(1162899410, f'Произошла ошибка: {ex}')
      