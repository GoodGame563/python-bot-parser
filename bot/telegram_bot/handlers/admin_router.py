from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, or_f, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F, types, Router

from kbds import reply
from data.telegram_channel_db import *
from logs.loging import log_admin_bot
from data.key_words_db import *
from handlers.filters import ChatTypeFilter, IsAdmin

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_router.message(StateFilter(None), CommandStart())
async def send_welcome(message: types.Message):
    log_admin_bot().send_debug(f"Received /start command from user: {message.from_user.id}")
    await message.answer("Привет, я бот для настройки бота-агрегатора новостей.", reply_markup=reply.main_menu_markup)

@admin_router.message(StateFilter(None), F.text.lower() == "назад")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'back' command from user: {message.from_user.id}")
    await message.answer("назад", reply_markup=reply.main_menu_markup)

@admin_router.message(StateFilter(None), F.text.lower() == "дополнительные возможности")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'дополнительные возможности' command from user: {message.from_user.id}")
    await message.answer("Перед вами представлен ряд дополнительных возможностей который вы можете выключить в данном парсере", reply_markup=reply.dop_vozmoc_markup)