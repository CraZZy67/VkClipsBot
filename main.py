from asyncio import run

from src.bot.global_classes import dp, bot
from src.logger import bot_logger
from src.bot import handler
from src.logger import bot_logger


dp.include_routers(handler.menu_router, handler.auth_router, handler.publics_router, 
                   handler.delete_router, handler.current_router, handler.queue_router)

async def main():
    await dp.start_polling(bot)    

if __name__ == "__main__":
    bot_logger.info("Бот запущен!")
    run(main())