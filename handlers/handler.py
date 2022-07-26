"""
Module for handlers
"""

from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot
from keyboards import start_kb, speciality_kb, additional_kb
from scrapers import get_vacancies, get_candidates


class FSMMain(StatesGroup):
    """a class to describe possible machine states"""

    speciality = State()
    additional_param = State()


async def start(message: Message):
    await bot.send_message(
        message.from_user.id,
        'Бот DjinniVacancies вітає вас!\n'
        'Тут ви можете отримати інформацію про вакансії з djinni.',
        reply_markup=start_kb
    )


async def link(message: Message):
    await bot.send_message(
        message.from_user.id,
        'https://djinni.co/jobs/',
        reply_markup=start_kb
    )


async def fetch(message: Message):
    await FSMMain.speciality.set()
    await bot.send_message(
        message.from_user.id,
        'Оберіть напрямок',
        reply_markup=speciality_kb
    )


async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        pass
    else:
        await state.finish()
    await message.answer('Canceled', reply_markup=start_kb)


async def ask_additional_parameter(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['speciality'] = message.text
    await FSMMain.next()
    await message.answer('Введіть додатковий параметр пошуку або команду ОК', reply_markup=additional_kb)


async def fetch_data(message: Message, state: FSMContext):
    vacancies_data = await get_vacancies(state, message.text)
    candidates_data = await get_candidates(state, message.text)

    async with state.proxy() as data:
        speciality = data['speciality']

    await FSMMain.speciality.set()
    await message.answer(
        speciality.replace('/', '').upper() + ': vacancies - ' + vacancies_data['total_number']
        + ', candidates - ' + candidates_data['total_number'] + '\n'
        'junior: vacancies - ' + vacancies_data['junior_number']
        + ', candidates - ' + candidates_data['junior_number'] + '\n'
        'middle: vacancies - ' + vacancies_data['middle_number']
        + ', candidates - ' + candidates_data['middle_number'] + '\n'
        'senior: vacancies - ' + vacancies_data['senior_number']
        + ', candidates - ' + candidates_data['senior_number'],
        reply_markup=speciality_kb
    )


async def echo(message: Message):
    text = 'Введіть одну з доступних команд!'
    await message.answer(text=text)


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
