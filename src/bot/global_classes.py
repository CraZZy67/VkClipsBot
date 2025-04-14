from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

import os

from src.objects.collector import Collector
from src.settings import Settings
from src.bot.utils import AutoStarter


load_dotenv()

dp = Dispatcher()
bot = Bot(os.getenv('TOKEN'))

settings = Settings()
collector = Collector(max_publics=settings.MAX_NUMBER_PUBLICS)

if len(os.listdir(f'.{settings.SLESH}{settings.STATES_PATH}')):
    collector.load_state()