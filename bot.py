"""
Main module
"""

from aiogram import executor

from create_bot import dp
from handlers import handler


handler.register_handlers_main(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
