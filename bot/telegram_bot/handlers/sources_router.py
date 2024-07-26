from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, or_f, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import F, types, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery

from kbds import reply
from logs.loging import log_admin_bot
from data.telegram_channel_db import telegram_db
from data.sites_db import site_db
from data.channels_db import return_channels
from handlers.filters import ChatTypeFilter, IsAdmin 

import itertools

admin_source_manage_router = Router()
admin_source_manage_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

tg_db = telegram_db("info")
s_db = site_db("info")
change_image = ""
page  = 0
step = 15

async def return_menu():
    telegram_channel = await tg_db.get_telegramm_channels() 
    global step
    global page
    menu = [[
            InlineKeyboardButton(text="<" if page > 0 else "", callback_data="In_First_button"),
            InlineKeyboardButton(text="🔄", callback_data="Reload"),
            InlineKeyboardButton(text=">" if page + step < len(telegram_channel) else "", callback_data="In_Second_button") 
        ]]
    return InlineKeyboardMarkup(inline_keyboard=menu)

@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "управление источниками")
async def source(message: types.Message):
    await message.answer("Выберете что-то одно", reply_markup=reply.sites_or_channels_markup)

@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "каналы")
async def source(message: types.Message):
    telegram_channel = await tg_db.get_telegramm_channels() 
    telegram_channel = dict(itertools.islice(telegram_channel.items(), page, page + step))
    if telegram_channel is not None or len(telegram_channel) != 0:
        channels_to_str = "".join ([f"- id:{id_channel}  @{telegram_channel[id_channel][0].split("/")[-1]}\n" for id_channel in telegram_channel])
        await message.answer(f"{channels_to_str}", reply_markup=await return_menu())
    await message.answer("Перед вами открылось меню в которое входит: редактирования, удаления, добавления, каналов для парсинга.", reply_markup=reply.manage_sources_markup)

@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "сайты")
async def source(message: types.Message):
    sites = await s_db.get_sites()
    text = "Доступные сайты\n"
    for site in sites:
        text += f"- {sites[site][0]}\n"
    await message.answer(text, disable_web_page_preview=True)
    await message.answer("Перед вами открылось меню в которое входит: удаления, добавления, сайтов для парсинга.", reply_markup=reply.manage_sites_markup, disable_web_page_preview=True)

class AddSite(StatesGroup):
    id = State()
    texts = {
        'AddChannel:id': 'Введите id канала заново',
    }

class DeleteSites(StatesGroup):
    id = State()
    texts = {
        'DeleteChannel:id': 'Введите id канала заново',
    }


@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "добавить сайт для парсинга")
async def add_channel1(message: types.Message, state: FSMContext):
    await message.answer("Введите url сайта", reply_markup= ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text ="/отмена"),] ],resize_keyboard=True))
    await state.set_state(AddSite.id)
    
@admin_source_manage_router.message(StateFilter(AddSite.id), F.text != "/отмена")
async def source(message: types.Message, state: FSMContext):
    await s_db.create_new_sites(message.text.replace(' ', ''))
    await state.clear()
    await message.answer("Успешно", reply_markup=reply.manage_sites_markup)
    
@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "удаление сайта для парсинга")
async def delete_channel1(message: types.Message, state: FSMContext):
    await message.answer("Введите url канала", reply_markup= ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text ="/отмена"),] ],resize_keyboard=True))
    await state.set_state(DeleteSites.id)

@admin_source_manage_router.message(StateFilter(DeleteSites.id), F.text != "/отмена")
async def source(message: types.Message, state: FSMContext):
    await s_db.delete_sites(message.text.replace(' ', ''))
    await state.clear()
    await message.answer("Успешно", reply_markup=reply.manage_sites_markup)

@admin_source_manage_router.callback_query(F.data == "In_Second_button")
async def query_right_page(callback_query: CallbackQuery):
    global step
    global page
    page += step
    telegram_channel = await tg_db.get_telegramm_channels()
    telegram_channel = dict(itertools.islice(telegram_channel.items(), page, page + step))
    channels_to_str = "".join ([f"- id:{id_channel}  @{telegram_channel[id_channel][0].split("/")[-1]}\n" for id_channel in telegram_channel])

    await callback_query.message.edit_text(f"{channels_to_str}", reply_markup=await return_menu())


@admin_source_manage_router.callback_query(F.data == "In_First_button")
async def query_left_page(callback_query: CallbackQuery):
    global page
    global step
    page -= step
    telegram_channel = await tg_db.get_telegramm_channels()
    telegram_channel = dict(itertools.islice(telegram_channel.items(), page, page + step))
    channels_to_str = "".join ([f"- id:{id_channel}  @{telegram_channel[id_channel][0].split("/")[-1]}\n" for id_channel in telegram_channel])

    await callback_query.message.edit_text(f"{channels_to_str}", reply_markup=await return_menu())

@admin_source_manage_router.callback_query(F.data == "Reload")
async def query_reload_page(callback_query: CallbackQuery):
    global page
    global step
    telegram_channel = await tg_db.get_telegramm_channels()
    telegram_channel = dict(itertools.islice(telegram_channel.items(), page, page + step))
    channels_to_str = "".join ([f"- id:{id_channel}  @{telegram_channel[id_channel][0].split("/")[-1]}\n" for id_channel in telegram_channel])
    if callback_query.message.text != channels_to_str[:-1]:
        await callback_query.message.edit_text(f"{channels_to_str}", reply_markup=await return_menu())
    else:
        await callback_query.answer("новых постов на страничке нет")


class AddSource(StatesGroup):
    id_field = State()
    url_field = State()

    texts = {
        'AddSource:id_field': 'Введите id канала заново',
        'AddSource:url_field': 'Введите url канала заново'
    }


@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "добавить источник для парсинга")
async def add_source(message: types.Message, state: FSMContext):
    log_admin_bot().send_debug(f"Received 'добавить источник для парсинга' command from user: {message.from_user.id}")
    await message.answer("Введите id канала, для отмены введите отмена", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddSource.id_field)

@admin_source_manage_router.message(StateFilter('*'), Command("отмена"))
@admin_source_manage_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=reply.telegram_menu_markup)

@admin_source_manage_router.message(AddSource.id_field, F.text)
async def add_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit:
        await message.answer("Поле id должно содержать только цифры \n Введите заново")
        return
    if len(message.text) != 10:
        await message.answer("Поле id должно быть по длине 10 символов \n Введите заново")
        return
    if await tg_db.get_telegram_channel_by_id(int(message.text)) is not None:
        await message.answer("Канал с таким id уже существует \n Введите заново")
        return
    await state.update_data(id_field=message.text)
    await message.answer("Введите url канала", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddSource.url_field)

@admin_source_manage_router.message(AddSource.id_field)
async def add_id2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")

@admin_source_manage_router.message(AddSource.url_field, F.text)
async def add_url(message: types.Message, state: FSMContext):
    tg_db = telegram_db("info")
    if not ("https://t.me/" in message.text):
        await message.answer("Поле url должно сооветствовать вот такому формату https://t.me/<название> \n Введите заново")
        return
    if await tg_db.get_telegram_channels_by_url(message.text.replace(" ","")) is not None:
        await message.answer("Канал с таким url уже существует \n Введите заново")
        return
    await state.update_data(url_field=message.text)
    await message.answer("Канал был добавлен в парсинг", reply_markup=reply.manage_sources_markup)
    data = await state.get_data()

    await tg_db.add_telegram_channel(data['url_field'], int(data['id_field']))

    await state.clear()

@admin_source_manage_router.message(AddSource.url_field)
async def add_url2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")

class ReductSource(StatesGroup):
    id_field_change = State()
    where_field_change = State()
    id_field = State()
    url_field = State()

    texts = {
        'ReductSource:id_field_change': 'Введите поле замены канала заново',
        'ReductSource:why_field_change': 'Введите поле замены канала заново',
        'ReductSource:id_field': 'Введите id канала заново',
        'ReductSource:url_field': 'Введите url канала заново',
    }

@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "редактировать источник для парсинга")
async def reduct_source(message: types.Message, state: FSMContext):
    log_admin_bot().send_debug(f"Received 'редактировать источник для парсинга' command from user: {message.from_user.id}")
    telegram_channel = await tg_db.get_telegramm_channels()
    if telegram_channel is None or len(telegram_channel) == 0:
        await message.answer("Каналов для парсинга не существует")
        await state.clear()
        return
    channels_to_str = "".join ([f"- id:{id_channel}  @{telegram_channel[id_channel][0].split("/")[-1]}\n" for id_channel in telegram_channel])
    text = "Каналы используемые для парсинга:\n" + channels_to_str
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Введите id канала который надо поменять", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ReductSource.id_field_change)


@admin_source_manage_router.message(ReductSource.id_field_change, F.text)
async def find_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit:
        await message.answer("Поле id должно содержать только цифры \n Введите заново")
        return
    if len(message.text) != 10:
        await message.answer("Поле id должно быть по длине 10 символов \n Введите заново")
        return
    if await tg_db.get_telegram_channel_by_id(int(message.text)) is None:
        await message.answer("Канал с таким id не существует \n Введите заново")
        return
    await state.update_data(id_field_change=message.text)
    await message.answer("Введите какое поле надо поменять 1:id 2:url")
    await state.set_state(ReductSource.where_field_change)

@admin_source_manage_router.message(ReductSource.id_field_change)
async def find_id2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")

@admin_source_manage_router.message(ReductSource.where_field_change, F.text)
async def which_field_change(message: types.Message, state: FSMContext):
    if not message.text.isdigit:
        await message.answer("Поле id должно содержать только цифры \n Введите заново")
        return
    elif int(message.text) == 1:
        await message.answer("Введите id:")
        await state.set_state(ReductSource.id_field)
        await state.update_data(where_field_change=message.text)
    elif int(message.text) == 2:
        await message.answer("Введите url:")
        await state.set_state(ReductSource.url_field)
        await state.update_data(where_field_change=message.text)
    else:
        await message.answer("Вы ввели не допустимые данные")

@admin_source_manage_router.message(ReductSource.id_field_change)
async def which_field_change2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")

@admin_source_manage_router.message(ReductSource.id_field, F.text)
async def reduct_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit:
        await message.answer("Поле id должно содержать только цифры \n Введите заново")
        return
    if len(message.text.replace(" ","")) != 10:
        await message.answer("Поле id должно быть по длине 10 символов \n Введите заново")
        return
    if await tg_db.get_telegram_channel_by_id(int(message.text)) is not None:
        await message.answer("Канал с таким id уже существует \n Введите заново")
        return
    await state.update_data(id_field=message.text)
    data = await state.get_data()
    await tg_db.update_id_telegram_channel(int(data.get("id_field_change")), int(data.get("id_field")))
    await state.clear()
    await message.answer("Канал был изменен", reply_markup=reply.manage_sources_markup)

@admin_source_manage_router.message(ReductSource.url_field, F.text)
async def reduct_url(message: types.Message, state: FSMContext):
    if not ("https://t.me/" in message.text):
        await message.answer("Поле url должно сооветствовать вот такому формату https://t.me/<название> \n Введите заново")
        return
    if await tg_db.get_telegram_channels_by_url(message.text.replace(" ","")) is not None:
        await message.answer("Канал с таким url уже существует \n Введите заново")
        return
    await state.update_data(url_field=message.text)
    await message.answer("Канал был изменен", reply_markup=reply.manage_sources_markup)
    data = await state.get_data()
    await tg_db.update_link_telegram_channel(int(data.get("id_field_change")), str(data.get("url_field")))
    await state.clear()

class DeleteSource(StatesGroup):
    id_field_delete = State()

    texts = {
        'ReductSource:id_field_change': 'Введите поле замены канала заново'
    }

@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "удаление источника для парсинга")
async def delete_source(message: types.Message, state: FSMContext):
    channels = await tg_db.get_telegramm_channels()
    if channels is None or len(channels) == 0:
        await message.answer("Каналов для парсинга не существует")
    channels_to_str = "".join ([f"- id:{id_channel}  @{channels[id_channel][0].split("/")[-1]}\n" for id_channel in channels])
    text = "Каналы используемые для парсинга:\n" + channels_to_str
    
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Введите id канала который надо удалить")
    await state.set_state(DeleteSource.id_field_delete)

@admin_source_manage_router.message(DeleteSource.id_field_delete, F.text)
async def delete_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit:
        await message.answer("Поле id должно содержать только цифры \n Введите заново")
        return
    if len(message.text) != 10:
        await message.answer("Поле id должно быть по длине 10 символов \n Введите заново")
        return
    if await tg_db.get_telegram_channel_by_id(int(message.text)) is None:
        await message.answer("Канал с таким id не существует \n Введите заново")
        return
    await state.update_data(id_field_delete=message.text)
    await message.answer("Канал был удален", reply_markup=reply.manage_sources_markup)
    data = await state.get_data()
    await tg_db.delete_telegram_channel(data.get("id_field_delete"))
    channels = await return_channels()
    for channel in channels:
        tg_db_time = telegram_db(channel)
        await tg_db_time.delete_telegram_channel(data.get("id_field_delete"))
    await state.clear()