import os

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_TOKEN = "6435271422:AAFS1XC7V7IJH7wuwG6-SHInrT2uUIgwSQk"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
