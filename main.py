from asyncio import run

from src.bot.global_classes import dp, bot
from src.logger import bot_logger
from src.bot import handler
from src.logger import bot_logger
import src.my_exceptions as my_exceptions


dp.include_routers(handler.menu_router, handler.auth_router, handler.publics_router, 
                   handler.delete_router, handler.current_router, handler.queue_router)

async def main():
    await dp.start_polling(bot)    

if __name__ == "__main__":
    bot_logger.info("Бот запущен!")
    
    try:
        run(main())
    except my_exceptions.WhileException as ex:
        bot_logger.error(f'Произошла ошибка в цикле паблика {ex.public_id}: {ex.exampler}')
        bot.send_message(1162899410, f'Произошла ошибка в цикле паблика {ex.public_id}: {ex.exampler}')
        
    except Exception as ex:
        bot_logger.error(f'Произошла ошибка: {ex}')
        bot.send_message(1162899410, f'Произошла ошибка: {ex}')
    