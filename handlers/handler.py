"""
Module for handlers
"""

import os

import redis
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import BotBlocked

import config
from create_bot import bot
from keyboards import start_kb, speciality_kb, additional_kb
from scrapers import get_vacancies, get_candidates


REDIS_HOST = os.getenv('REDIS_HOST')
# REDIS_HOST = config.REDIS_HOST
REDIS_PORT = 6379
REDIS_DB = 0


class FSMMain(StatesGroup):
    """a class to describe possible machine states"""

    speciality = State()
    additional_param = State()


async def start(message: Message):
    try:
        await bot.send_message(
            message.from_user.id,
            'Бот DjinniVacancies вітає вас!\n'
            'Тут ви можете отримати інформацію про вакансії з djinni.',
            reply_markup=start_kb
        )
    except BotBlocked:
        print('Forbidden: bot was blocked by the user')


async def link(message: Message):
    try:
        await bot.send_message(
            message.from_user.id,
            'https://djinni.co/jobs/',
            reply_markup=start_kb
        )
    except BotBlocked:
        print('Forbidden: bot was blocked by the user')


async def fetch(message: Message):
    try:
        await FSMMain.speciality.set()
        await bot.send_message(
            message.from_user.id,
            'Оберіть напрямок',
            reply_markup=speciality_kb
        )
    except BotBlocked:
        print('Forbidden: bot was blocked by the user')


async def cancel(message: Message, state: FSMContext):
    try:
        current_state = await state.get_state()
        if current_state is None:
            pass
        else:
            await state.finish()
        await message.answer('Canceled', reply_markup=start_kb)
    except BotBlocked:
        print('Forbidden: bot was blocked by the user')


async def ask_additional_parameter(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['speciality'] = message.text
        await FSMMain.next()
        await message.answer('Введіть додатковий параметр пошуку або команду ОК', reply_markup=additional_kb)
    except BotBlocked:
        print('Forbidden: bot was blocked by the user')


async def fetch_data(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            speciality = data['speciality']
        await FSMMain.speciality.set()

        redis_key = speciality + '.' + message.text
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB) as redis_client:
            if redis_client.exists(redis_key):
                await message.answer(redis_client.get(name=redis_key).decode('utf-8'), reply_markup=speciality_kb)
                return

        vacancies_data = await get_vacancies(state, message.text)
        candidates_data = await get_candidates(state, message.text)

        answer = speciality.replace('/', '').upper() + ': vacancies - ' + vacancies_data['total_number'] \
                 + ', candidates - ' + candidates_data['total_number'] + '\n' \
                 + 'junior: vacancies - ' + vacancies_data['junior_number'] \
                 + ', candidates - ' + candidates_data['junior_number'] + '\n' \
                 + 'middle: vacancies - ' + vacancies_data['middle_number'] \
                 + ', candidates - ' + candidates_data['middle_number'] + '\n' \
                 + 'senior: vacancies - ' + vacancies_data['senior_number'] \
                 + ', candidates - ' + candidates_data['senior_number']
        await message.answer(answer, reply_markup=speciality_kb)
        with redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB) as redis_client:
            redis_client.set(name=redis_key, value=answer, ex=60)

    except BotBlocked:
        print('Forbidden: bot was blocked by the user')


async def echo(message: Message):
    try:
        text = 'Введіть одну з доступних команд!'
        await message.answer(text=text)
    except BotBlocked:
        print('Forbidden: bot was blocked by the user')


def register_handlers_main(dp: Dispatcher):
    """Procedure for handlers registration"""

    dp.register_message_handler(start, commands=['Start', 'help'])
    dp.register_message_handler(link, commands=['Link'])
    dp.register_message_handler(fetch, commands=['Fetch'], state=None)
    dp.register_message_handler(cancel, state='*', commands=['Cancel'])
    dp.register_message_handler(ask_additional_parameter, state=FSMMain.speciality, commands=[
        'Python',
        'Ruby',
        'PHP',
        'Java',
        'JavaScript',
    ])
    dp.register_message_handler(fetch_data, state=FSMMain.additional_param)
    dp.register_message_handler(echo)
