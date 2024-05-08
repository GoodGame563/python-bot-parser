import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, or_f, Command

from kbds import reply

bot = Bot(token='7064443400:AAGYVAtnIDmJRGEnZ89hzzqjYvKJV5zNAZI')

dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Привет, я бот для настройки бота-агрегатора новостей.", reply_markup= reply.main_menu_markup)

@dp.message(or_f(Command("edit"), (F.text.lower() == "Меню редактирования")))
async def source(message: types.Message):
    await message.answer("Перед вами открылось меню для редактирвоания в которое входит редактирования источников для парсинга.", reply_markup= reply.manage_sources_markup)

@dp.message(or_f(Command("add"), (F.text.lower() == "Меню редактирования")))
async def source(message: types.Message):
    await message.answer("Перед вами открылось меню для редактирвоания в которое входит добавление источников для парсинга.", reply_markup= reply.manage_sources_markup)

@dp.message(or_f(Command("delet"), (F.text.lower() == "Меню редактирования")))
async def source(message: types.Message):
    await message.answer("Перед вами открылось меню для редактирвоания в которое входит удаление источников для парсинга.", reply_markup= reply.manage_sources_markup)

@dp.message(or_f(Command("time"), (F.text.lower() == "Время работы")))
async def source(message: types.Message):
    await message.answer("Выставите время работы для бота", reply_markup= reply.manage_sources_markup)

@dp.message(or_f(Command("timeoff"), (F.text.lower() == "Время работы")))
async def source(message: types.Message):
    await message.answer("Выключить режим работы бота", reply_markup= reply.manage_sources_markup)

@dp.message(or_f(Command("back"), (F.text.lower() == "Назад")))
async def source(message: types.Message):
    await message.answer("назад", reply_markup= reply.manage_sources_markup)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())