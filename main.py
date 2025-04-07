from asyncio import run, create_task

from src.bot.global_classes import dp, bot
from src.logger import bot_logger
from src.bot import handler
from src.logger import bot_logger
from src.bot.utils import intercept_expiry
from src.settings import Settings


dp.include_routers(handler.menu_router, handler.auth_router, handler.publics_router, 
                   handler.delete_router, handler.current_router, handler.queue_router)
settings = Settings()

async def main():
    create_task(intercept_expiry(settings.REFRESH_TOKEN_INTERVAL))
    await dp.start_polling(bot)    

if __name__ == "__main__":
    bot_logger.info("Бот запущен!")
    run(main())

    