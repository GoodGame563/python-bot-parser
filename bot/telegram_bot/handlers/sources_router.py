from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, or_f, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F, types, Router

from kbds import reply
from data.telegram_channel_db import *
from logs.loging import log_admin_bot
from data.telegram_channel_db import *
from handlers.filters import ChatTypeFilter, IsAdmin 

admin_source_manage_router = Router()
admin_source_manage_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "управление источниками")
async def source(message: types.Message):
    await message.answer("Перед вами открылось меню в которое входит: редактирования, удаления, добавления, источников для парсинга.", reply_markup=reply.manage_sources_markup)


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
    await message.answer("Действия отменены", reply_markup=reply.main_menu_markup)

@admin_source_manage_router.message(AddSource.id_field, F.text)
async def add_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit:
        await message.answer("Поле id должно содержать только цифры \n Введите заново")
        return
    if len(message.text) != 10:
        await message.answer("Поле id должно быть по длине 10 символов \n Введите заново")
        return
    if await get_telegram_channel_by_id(int(message.text)) is not None:
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
    if not ("https://t.me/" in message.text):
        await message.answer("Поле url должно сооветствовать вот такому формату https://t.me/<название> \n Введите заново")
        return
    if await get_telegram_channels_by_url(message.text.replace(" ","")) is not None:
        await message.answer("Канал с таким url уже существует \n Введите заново")
        return
    await state.update_data(url_field=message.text)
    await message.answer("Канал был добавлен в парсинг", reply_markup=reply.manage_sources_markup)
    data = await state.get_data()
    await add_telegram_channel(data['url_field'], int(data['id_field']))
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
    telegram_channel =await get_telegramm_channels()
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
    if await get_telegram_channel_by_id(int(message.text)) is None:
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
    if await get_telegram_channel_by_id(int(message.text)) is not None:
        await message.answer("Канал с таким id уже существует \n Введите заново")
        return
    await state.update_data(id_field=message.text)
    data = await state.get_data()
    await update_id_telegram_channel(int(data.get("id_field_change")), int(data.get("id_field")))
    await state.clear()
    await message.answer("Канал был изменен", reply_markup=reply.manage_sources_markup)

@admin_source_manage_router.message(ReductSource.url_field, F.text)
async def reduct_url(message: types.Message, state: FSMContext):
    if not ("https://t.me/" in message.text):
        await message.answer("Поле url должно сооветствовать вот такому формату https://t.me/<название> \n Введите заново")
        return
    if await get_telegram_channels_by_url(message.text.replace(" ","")) is not None:
        await message.answer("Канал с таким url уже существует \n Введите заново")
        return
    await state.update_data(url_field=message.text)
    await message.answer("Канал был изменен", reply_markup=reply.manage_sources_markup)
    data = await state.get_data()
    await update_link_telegram_channel(int(data.get("id_field_change")), str(data.get("url_field")))
    await state.clear()

class DeleteSource(StatesGroup):
    id_field_delete = State()

    texts = {
        'ReductSource:id_field_change': 'Введите поле замены канала заново'
    }

@admin_source_manage_router.message(StateFilter(None), F.text.lower() == "удаление источника для парсинга")
async def delete_source(message: types.Message, state: FSMContext):
    channels = await get_telegramm_channels()
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
    if await get_telegram_channel_by_id(int(message.text)) is None:
        await message.answer("Канал с таким id не существует \n Введите заново")
        return
    await state.update_data(id_field_delete=message.text)
    await message.answer("Канал был удален", reply_markup=reply.manage_sources_markup)
    data = await state.get_data()
    await delete_telegram_channel(data.get("id_field_delete"))
    await state.clear()