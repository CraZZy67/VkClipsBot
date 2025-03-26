from asyncio import run, create_task

from src.bot.global_classes import dp, bot
from src.logger import bot_logger
from src.bot.handler.menu import menu_router
from src.bot.handler.authorization import auth_router
from src.bot.handler.publics import publics_router


dp.include_routers(menu_router, auth_router, publics_router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    bot_logger.info("Бот запущен!")
    run(main())