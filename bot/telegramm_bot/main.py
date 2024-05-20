import asyncio 
import os
import sys
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.strategy import FSMStrategy
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, or_f, Command, StateFilter
from work_to_parse import start_parsing
from kbds import reply
from dotenv import load_dotenv
from data.telegram_channel_db import *

sys.path.append(os.path.join(os.getcwd(), '..'))

from logs.loging import log_admin_bot

load_dotenv()
bot_token = os.environ.get('BOT_TOKEN')
if bot_token is None or bot_token == '':
    log_admin_bot().send_critical('Bot token missing')
    assert ()
else:
    log_admin_bot().send_info('Bot token is set')
bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    log_admin_bot().send_debug(f"Received /start command from user: {message.from_user.id}")
    await message.answer("Привет, я бот для настройки бота-агрегатора новостей.", reply_markup=reply.main_menu_markup)

#вот этот код надо повторить минтик
class AddSource(StatesGroup):
    id_field = State()
    url_field = State()
    

    texts = {
        'AddSource:id_field': 'Введите id канала заново',
        'AddSource:url_field': 'Введите url канала заново'
    }

@dp.message(F.text.lower() == "управление источниками")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'управление источниками' command from user: {message.from_user.id}")
    await message.answer("Перед вами открылось меню в которое входит: редактирования, удаления, добавления, источников для парсинга.", reply_markup=reply.manage_sources_markup)

@dp.message(StateFilter(None), F.text.lower() == "добавить источник для парсинга")
async def source(message: types.Message, state: FSMContext):
    log_admin_bot().send_debug(f"Received 'добавить источник для парсинга' command from user: {message.from_user.id}")
    await message.answer("Введите id канала", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddSource.id_field)

@dp.message(AddSource.id_field, F.text)
async def add_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit:
        await message.answer("Поле id должно содержать только цифры \n Введите заново")
        return
    if len(message.text) != 10:
        await message.answer("Поле id должно быть по длине 10 символов \n Введите заново")
        return
    if get_telegram_channel_by_id(int(message.text)) is not None:
        await message.answer("Канал с таким id уже существует \n Введите заново")
        return
    await state.update_data(id_field=message.text)
    await message.answer("Введите url канала")
    await state.set_state(AddSource.url_field)

@dp.message(AddSource.id_field)
async def add_id2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")

@dp.message(AddSource.url_field, F.text)
async def add_url(message: types.Message, state: FSMContext):
    if not ("https://t.me/" in message.text):
        await message.answer("Поле url должно сооветствовать вот такому формату https://t.me/<название> \n Введите заново")
        return
    if get_telegram_channels_by_url(message.text.replace(" ","")) is not None:
        await message.answer("Канал с таким url уже существует \n Введите заново")
        return
    await state.update_data(url_field=message.text)
    await message.answer("Канал был добавлен в парсинг", reply_markup=reply.manage_sources_markup)
    data = await state.get_data()
    add_telegram_channel(data['url_field'], int(data['id_field']))
    await state.clear()

@dp.message(AddSource.url_field)
async def add_url2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")

#вот тут он кончается


@dp.message(F.text.lower() == "back")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'back' command from user: {message.from_user.id}")
    await message.answer("назад", reply_markup=reply.main_menu_markup)

@dp.message(F.text.lower() == "фильтрация постов источника")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'фильтрация постов источника' command from user: {message.from_user.id}")
    await message.answer("Перед вами открылось меню для редактирвания в которое входит добавление источников для парсинга.", reply_markup=reply.filter_post_markup)

@dp.message(F.text.lower() == "редактирование поста")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'редактирование поста' command from user: {message.from_user.id}")
    await message.answer("Перед вами открылось меню для редактирвоания поста где контролируются картинки,гиперссылки.", reply_markup=reply.edit_post_markup)

@dp.message(F.text.lower() == "расписание работы")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'расписание работы' command from user: {message.from_user.id}")
    await message.answer("Выставите время работы для бота", reply_markup=reply.time_markup)

@dp.message(F.text.lower() == "добавить расписание работы бота")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'добавить расписание работы бота' command from user: {message.from_user.id}")
    await message.answer("Выставите время работы для бота", reply_markup=reply.raspisanie_markup)

@dp.message(F.text.lower() == "добавить источник для парсинга")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'добавить источник для парсинга' command from user: {message.from_user.id}")
    await message.answer("Вы дожны выбрать из какого источника будет парситься статья", reply_markup=reply.razdel_tg_sait_markup)

@dp.message(F.text.lower() == "дополнительные возможности")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'дополнительные возможности' command from user: {message.from_user.id}")
    await message.answer("Перед вами представлен ряд дополнительных возможностей который вы можете выключить в данном парсере", reply_markup=reply.dop_vozmoc_markup)

@dp.message(F.text.lower() == "введите ключевые слова для фильтра")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'введите ключевые слова для фильтра' command from user: {message.from_user.id}")
    await message.answer("Добовляйте пожалуйста ключевые слова через пробел",)

@dp.message(F.text)
async def text(message: types.Message):
    log_admin_bot().send_debug(f"Received text message from user: {message.from_user.id} with text: {message.text}")
    await message.answer("Новые данные успешно сохранены и с этого момента вступили в силу ", reply_markup=reply.filter_post_markup)


async def main():
    task1 = asyncio.create_task(dp.start_polling(bot))
    task2 = asyncio.create_task(start_parsing())

    await asyncio.gather(task1, task2)
    log_admin_bot().send_info("bot started")
    

asyncio.run(main()) 