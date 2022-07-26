"""
Module for keyboards creating
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# start keyboard
button_fetch = KeyboardButton('/Fetch')
button_link = KeyboardButton('/Link')

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.row(button_fetch, button_link)

# speciality keyboard
button_python = KeyboardButton('/Python')
button_ruby = KeyboardButton('/Ruby')
button_php = KeyboardButton('/PHP')

button_java = KeyboardButton('/Java')
button_c_ = KeyboardButton('/JavaScript')

button_cancel = KeyboardButton('/Cancel')

speciality_kb = ReplyKeyboardMarkup(resize_keyboard=True)
speciality_kb.row(button_python, button_ruby, button_php)
speciality_kb.row(button_java, button_c_)
speciality_kb.add(button_cancel)

# additional keyboard
button_ok = KeyboardButton('/OK')

additional_kb = ReplyKeyboardMarkup(resize_keyboard=True)
additional_kb.row(button_ok, button_cancel)






