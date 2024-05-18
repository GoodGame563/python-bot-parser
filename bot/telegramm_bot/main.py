import asyncio 
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, or_f, Command

from kbds import reply

bot = Bot(token='7064443400:AAGYVAtnIDmJRGEnZ89hzzqjYvKJV5zNAZI')
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Привет, я бот для настройки бота-агрегатора новостей.", reply_markup= reply.main_menu_markup)

@dp.message(F.text.lower() == "back")
async def source(message: types.Message):
    await message.answer("назад", reply_markup= reply.main_menu_markup)

@dp.message(F.text.lower() == "управление источниками")
async def source(message: types.Message):
    await message.answer("Перед вами открылось меню в которое входит: редактирования, удаления, добовлния, источников для парсинга.", reply_markup= reply.manage_sources_markup)

@dp.message(F.text.lower() == "фильтрация постов источника")
async def source(message: types.Message):
    await message.answer("Перед вами открылось меню для редактирвания в которое входит добавление источников для парсинга.", reply_markup= reply.filter_post_markup)

@dp.message(F.text.lower() == "редактирование поста")
async def source(message: types.Message):
    await message.answer("Перед вами открылось меню для редактирвоания поста где контролируются картинки,гиперссылки.", reply_markup= reply.edit_post_markup)

@dp.message(F.text.lower() == "расписание работы")
async def source(message: types.Message):
    await message.answer("Выставите время работы для бота", reply_markup= reply.time_markup)

@dp.message(F.text.lower() == "добавить расписание работы бота")
async def source(message: types.Message):
    await message.answer("Выставите время работы для бота", reply_markup= reply.raspisanie_markup)

@dp.message(F.text.lower() == "добавить источник для парсинга")
async def source(message: types.Message):
    await message.answer("Вы дожны выбрать из какого источника будет парситься статья", reply_markup= reply.razdel_tg_sait_markup)

@dp.message(F.text.lower() == "дополнительные возможности")
async def source(message: types.Message):
    await message.answer("Перед вами представлен ряд дополнительных возможностей который вы можете выключить в данном парсере", reply_markup= reply.dop_vozmoc_markup)

@dp.message(F.text.lower() == "введите ключевые слова для фильтра")
async def source(message: types.Message):
    await message.answer("Добовляйте пожалуйста ключевые слова через пробел", )

@dp.message(F.text)
async def text(message: types.Message):
    await message.answer("Новые данные успешно сохранены и  с этого момента вступили в силу ", reply_markup= reply.filter_post_markup)

async def main():
    await dp.start_polling(bot)
    

asyncio.run(main()) 