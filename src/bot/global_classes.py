from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

import os

from src.objects.collector import Collector
from src.settings import Settings


load_dotenv()

settings = Settings()
dp = Dispatcher()
bot = Bot(os.getenv('TOKEN'))

collector = Collector(max_publics=settings.MAX_NUMBER_PUBLICS)

if len(os.listdir(f'.{settings.SLESH}{settings.STATES_PATH}')):
    collector.load_state()