import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, or_f, Command

from kbds import reply

bot = Bot(token='7064443400:AAGYVAtnIDmJRGEnZ89hzzqjYvKJV5zNAZI')

dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Привет, я бот для настройки бота-агрегатора новостей.", reply_markup= reply.main_menu_markup)

@dp.message(or_f(Command("reply"), (F.text.lower() == "управление источниками")))
async def source(message: types.Message):
    await message.answer("sdfsdfsdf", reply_markup= reply.manage_sources_markup)


async def main():
    await dp.start_polling(bot)

asyncio.run(main())