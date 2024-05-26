from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, or_f, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F, types, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery

from kbds import reply
from data.settings_db import *
from logs.loging import log_admin_bot
from handlers.filters import ChatTypeFilter, IsAdmin

admin_settings_manage_router = Router()
admin_settings_manage_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

change_image = "change_image"
change_link = "change_link"
change_time = "change_time"
change_network = "change_network"
change_parser = "change_parser"
change_post = "change_post"
change_work = "change_work"

async def create_text():
    settings = await get_all_settings()
    if settings is not None:
        text = "⚙️ Настройки постов: "
        text += "\nПостинг вместе с фотографиями "+ ("✅" if settings.get('posting_image') and settings.get('posting_image') is not None else "❌")
        text += "\nОставлять ссылку на первоисточник " + ("✅" if settings.get('link_to_source') and settings.get('posting_image') is not None else "❌")
        text += "\n\nНастройка времени бота:"
        text += "\nРабота бота в течении определенного времени " + ("✅" if settings.get('work_on_time') and settings.get('work_on_time') is not None else "❌")
        text += f"\n⏳ Начало постинга {settings.get('start_time').strftime('%H:%M:%S')} \n⏳ Конец постинга {settings.get('end_time').strftime('%H:%M:%S')}" if settings.get('work_on_time') else ""
        text += "\n\nНастройка элементов бота: " 
        text += "\nПарсинг " + ("✅" if settings.get('parser') and settings.get('parser') is not None else "❌")
        text += "\nОтправка постов " + ("✅" if settings.get('send_post') and settings.get('send_post') is not None else "❌")
        text += "\nОбработка нейросетью " + ("✅" if settings.get('neural_enabled') and settings.get('neural_enabled') is not None else "❌")
        return text

async def create_menu():
    settings = await get_all_settings()
    if settings is not None:
        post_image = settings.get('posting_image')
        link = settings.get('link_to_source')
        time = settings.get('work_on_time')
        parser = settings.get('parser')
        posting = settings.get('send_post')
        neural = settings.get('neural_enabled')
        menu = [
        [InlineKeyboardButton(text=("Включить" if not post_image else "Отключить") + " фото", callback_data=change_image),
        InlineKeyboardButton(text=("Включить" if not link else "Отключить") + " ссылку", callback_data=change_link)],
        [InlineKeyboardButton(text=("Включить" if not time else "Отключить") + " время работы", callback_data=change_time)],
        [InlineKeyboardButton(text=("Включить" if not neural else "Отключить") + " нейросеть", callback_data=change_network),
        InlineKeyboardButton(text=("Включить" if not parser else "Отключить") + " парсер", callback_data=change_parser)],
        [InlineKeyboardButton(text=("Включить" if not posting else "Отключить") + " постинг", callback_data=change_post)],
        [InlineKeyboardButton(text="Полностью отключить бота" if parser or neural or posting else "Полностью включить бота", callback_data=change_work)]
        ]
        return menu


@admin_settings_manage_router.message(StateFilter(None), F.text.lower() == "настройки")
async def source(message: types.Message):
    log_admin_bot().send_debug(f"Received 'настройки' command from user: {message.from_user.id}")
    menu = InlineKeyboardMarkup(inline_keyboard= await create_menu())
    await message.answer(await create_text(), reply_markup=menu)

@admin_settings_manage_router.callback_query(F.data == change_image)
async def query_change_image(callback_query: CallbackQuery):
    settings = await get_all_settings()
    await switch_mode_send_image(not settings.get('posting_image'))
    await callback_query.message.edit_text(await create_text(), reply_markup=InlineKeyboardMarkup(inline_keyboard=await create_menu()))

@admin_settings_manage_router.callback_query(F.data == change_link)
async def query_change_date(callback_query: CallbackQuery):
    settings = await get_all_settings()
    await switch_mode_send_links(not settings.get('link_to_source'))
    await callback_query.message.edit_text(await create_text(), reply_markup=InlineKeyboardMarkup(inline_keyboard=await create_menu()))

@admin_settings_manage_router.callback_query(F.data == change_network)
async def query_change_date(callback_query: CallbackQuery):
    settings = await get_all_settings()
    await switch_mode_neural_network(not settings.get('neural_enabled'))
    await callback_query.message.edit_text(await create_text(), reply_markup=InlineKeyboardMarkup(inline_keyboard=await create_menu()))

@admin_settings_manage_router.callback_query(F.data == change_parser)
async def query_change_date(callback_query: CallbackQuery):
    settings = await get_all_settings()
    await switch_mode_parser(not settings.get('parser'))
    await callback_query.message.edit_text(await create_text(), reply_markup=InlineKeyboardMarkup(inline_keyboard=await create_menu()))

@admin_settings_manage_router.callback_query(F.data == change_post)
async def query_change_date(callback_query: CallbackQuery):
    settings = await get_all_settings()
    await switch_mode_send_post(not settings.get('send_post'))
    await callback_query.message.edit_text(await create_text(), reply_markup=InlineKeyboardMarkup(inline_keyboard=await create_menu()))

@admin_settings_manage_router.callback_query(F.data == change_work)
async def query_change_date(callback_query: CallbackQuery):
    settings = await get_all_settings()
    parser = settings.get('parser')
    posting = settings.get('send_post')
    neural = settings.get('neural_enabled')
    final = parser or posting or neural
    await switch_mode_send_post(not final)
    await switch_mode_neural_network(not final)
    await switch_mode_parser(not final)
    await callback_query.message.edit_text(await create_text(), reply_markup=InlineKeyboardMarkup(inline_keyboard=await create_menu()))

class AddTime(StatesGroup):
    start_time = State()
    end_time = State()

    texts = {
        'AddSource:start_time': 'Введите id канала заново',
        'AddSource:end_tim': 'Введите url канала заново'
    }

@admin_settings_manage_router.callback_query(F.data == change_time)
async def query_change_date(callback_query: CallbackQuery, state: FSMContext):
    settings = await get_all_settings()
    if bool(settings.get('work_on_time')):
        await turn_off_work_on_time()
        await callback_query.message.edit_text(await create_text(), reply_markup=InlineKeyboardMarkup(inline_keyboard=await create_menu()))
    else:
        await callback_query.answer("Отправьте начало времени работы бота (пример hh:mm:ss) \nдля отмены напишите отмена", show_alert=True)
        await state.set_state(AddTime.start_time)


@admin_settings_manage_router.message(StateFilter(AddTime.start_time), F.text.contains(':'))
async def source(message: types.Message, state: FSMContext):
    log_admin_bot().send_debug(f"Received 'дополнительные возможности' command from user: {message.from_user.id}")
    if len(message.text.split(':')) != 3:
        await message.answer("Напишите время правильного формата")
        return
    if not str(message.text.split(':')[0]).isdigit():
        await message.answer("Напишите часы правильного формата")
        return
    if not str(message.text.split(':')[1]).isdigit():
        await message.answer("Напишите минуты правильного формата")
        return
    if not str(message.text.split(':')[2]).isdigit():
        await message.answer("Напишите секунды правильного формата")
        return
    if int(message.text.split(':')[0]) < 0 or int(message.text.split(':')[0]) > 24:
        await message.answer("Напишите часы правильного формата")
        return
    if int(message.text.split(':')[1]) < 0 or int(message.text.split(':')[1]) > 60:
        await message.answer("Напишите минуты правильного формата")
        return
    if int(message.text.split(':')[2]) < 0 or int(message.text.split(':')[2]) > 60:
        await message.answer("Напишите секунды правильного формата")
        return
    settings = await get_all_settings()
    if not bool(settings.get('work_on_time')):
        await state.update_data(start_time=datetime.datetime.strptime(message.text,'%H:%M:%S'))
        await state.set_state(AddTime.end_time)
        await message.answer("Напишите конец времени работы бота (для отмены напишите отмена)")

@admin_settings_manage_router.message(StateFilter(AddTime.start_time), F)
async def source1(message: types.Message, state: FSMContext):
    await message.answer("Напишите время правильного формата для отмены напишите отмена", reply_markup=ReplyKeyboardRemove)

@admin_settings_manage_router.message(StateFilter(AddTime.end_time), F.text.contains(':'))
async def source(message: types.Message, state: FSMContext):
    log_admin_bot().send_debug(f"Received 'дополнительные возможности' command from user: {message.from_user.id}")
    if len(message.text.split(':')) != 3:
        await message.answer("Напишите время правильного формата")
        return
    if not str(message.text.split(':')[0]).isdigit():
        await message.answer("Напишите часы правильного формата")
        return
    if not str(message.text.split(':')[1]).isdigit():
        await message.answer("Напишите минуты правильного формата")
        return
    if not str(message.text.split(':')[2]).isdigit():
        await message.answer("Напишите секунды правильного формата")
        return
    if int(message.text.split(':')[0]) < 0 or int(message.text.split(':')[0]) > 24:
        await message.answer("Напишите часы правильного формата")
        return
    if int(message.text.split(':')[1]) < 0 or int(message.text.split(':')[1]) > 60:
        await message.answer("Напишите минуты правильного формата")
        return
    if int(message.text.split(':')[2]) < 0 or int(message.text.split(':')[2]) > 60:
        await message.answer("Напишите секунды правильного формата")
        return
    settings = await get_all_settings()
    if not bool(settings.get('work_on_time')):
        await state.update_data(end_time=datetime.datetime.strptime(message.text,'%H:%M:%S'))
        data = await state.get_data()
        await turn_on_work_on_time(data.get('start_time'), data.get('end_time')) 
        await state.clear()
        await message.answer("Успешно")
