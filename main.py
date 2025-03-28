from asyncio import run

from src.bot.global_classes import dp, bot
from src.logger import bot_logger
from src.bot.handler.menu import menu_router
from src.bot.handler.authorization import auth_router
from src.bot.handler.publics import publics_router
from src.bot.handler.delete import delete_router
from src.bot.handler.current import current_router
from src.bot.handler.queue import queue_router



dp.include_routers(menu_router, auth_router, publics_router, 
                   delete_router, current_router, queue_router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    bot_logger.info("Бот запущен!")
    run(main())