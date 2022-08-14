"""
Module for bot creating
"""

import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

storage = MemoryStorage()


bot = Bot(token=os.getenv('TOKEN'))
# bot = Bot(token=config.TOKEN)


dp = Dispatcher(bot, storage=storage)
