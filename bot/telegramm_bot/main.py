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
from data.settings_db import *
from work_to_post_in_channel import print_post
from logs.loging import log_admin_bot
from sources import admin_source_manage_router
from key_words import admin_key_words_manage_router
from data.base_connection_db import *


sys.path.append(os.path.join(os.getcwd(), '..'))
load_dotenv()


bot_token = os.environ.get('BOT_TOKEN')
if bot_token is None or bot_token == '':
    log_admin_bot().send_critical('Bot token missing')
    assert ()
else:
    log_admin_bot().send_info('Bot token is set')


bot = Bot(token=bot_token)

dp = Dispatcher()

dp.include_routers(admin_source_manage_router)
dp.include_routers(admin_key_words_manage_router)

@dp.message(StateFilter(None), CommandStart())
async def send_welcome(message: types.Message):
    log_admin_bot().send_debug(f"Received /start command from user: {message.from_user.id}")
    await message.answer("Привет, я бот для настройки бота-агрегатора новостей.", reply_markup=reply.main_menu_markup)

@dp.message(StateFilter(None), F.text.lower() == "назад")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'back' command from user: {message.from_user.id}")
    await message.answer("назад", reply_markup=reply.main_menu_markup)

@dp.message(StateFilter(None), F.text.lower() == "редактирование поста")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'редактирование поста' command from user: {message.from_user.id}")
    await message.answer("Перед вами открылось меню для редактирвоания поста где контролируются картинки,гиперссылки.", reply_markup=reply.edit_post_markup)

@dp.message(StateFilter(None), F.text.lower() == "расписание работы")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'расписание работы' command from user: {message.from_user.id}")
    await message.answer("Выставите время работы для бота", reply_markup=reply.time_markup)

@dp.message(StateFilter(None), F.text.lower() == "добавить расписание работы бота")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'добавить расписание работы бота' command from user: {message.from_user.id}")
    await message.answer("Выставите время работы для бота", reply_markup=reply.raspisanie_markup)


@dp.message(StateFilter(None), F.text.lower() == "дополнительные возможности")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'дополнительные возможности' command from user: {message.from_user.id}")
    await message.answer("Перед вами представлен ряд дополнительных возможностей который вы можете выключить в данном парсере", reply_markup=reply.dop_vozmoc_markup)



async def main():
    while True:
        if get_url_connection() is None:
            log_admin_bot().send_critical("Нет соединения с базой данных")
            log_admin_bot().send_info("Попытка подсоединения к базе данных")
            await asyncio.sleep(60)
            return
        break
    set_basic_parameters()
    task1 = asyncio.create_task(dp.start_polling(bot))
    #task2 = asyncio.create_task(start_parsing())
    #task3 = asyncio.create_task(print_post(bot))

    #await asyncio.gather(task1, task2, task3)
    await asyncio.gather(task1)
    log_admin_bot().send_info("bot started")
    

asyncio.run(main()) 