from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, or_f, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F, Bot, types, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters.callback_data import CallbackData

from aiogram.fsm.context import FSMContext
from kbds import reply
from data.settings_db import *
from data.sites_db import *
from logs.loging import log_admin_bot
from handlers.filters import ChatTypeFilter, IsAdmin
from data.channels_db import *
from data.telegram_channel_db import telegram_db
from data.key_words_db import *
from handlers.filters import *
admin_channels_manage_router = Router()
admin_channels_manage_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

class MyCallback(CallbackData, prefix ="my"):
    id:int

channel = "info"

async def create_text():
    channels = await return_channels_with_name()
    text = "Каналы : \n"
    for id_channel, channel_name in channels:
        text += f"- id: {id_channel}  {channel_name}\n"
    return text

async def create_menu():
    channels = await return_channels()
    buttons = []
    i_channel = 0
    while i_channel < len(channels):
        if i_channel + 1 < len(channels):
            buttons.append([InlineKeyboardButton(text=channels[i_channel], callback_data=MyCallback(id = channels[i_channel]).pack()), InlineKeyboardButton(text=channels[i_channel+1], callback_data=MyCallback(id = channels[i_channel+1]).pack())])
        else:
            buttons.append([InlineKeyboardButton(text=channels[i_channel], callback_data=MyCallback(id = channels[i_channel]).pack())])
        i_channel += 2
    menu = buttons
    return InlineKeyboardMarkup(inline_keyboard=menu)

async def create_menu_channel(id):
    buttons = [
        [InlineKeyboardButton(text="Управлять источниками", callback_data="reduct_channel")],
        [InlineKeyboardButton(text="Управлять сайтами", callback_data="reduct_site")],
        [InlineKeyboardButton(text="Настройки", callback_data=SettingsCallback(id=id, back= False).pack())],
        [InlineKeyboardButton(text="Назад", callback_data="main")],
        ]
    menu = buttons
    return InlineKeyboardMarkup(inline_keyboard=menu)

async def create_menu_channels():
    tg_db = telegram_db("info")
    global channel
    channels = await tg_db.get_telegramm_channels()
    buttons = []  
    used_channels = await return_in_channel_channels(channel)
    
    for channel2 in used_channels:
        
        if int(channel2[0]) in channels:
            del channels[int(channel2[0])]
    
    for channel1 in channels:
        buttons.append([InlineKeyboardButton(text=f"{channels[channel1][0]}", callback_data=TelegramCallback(id=channel1).pack())])
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back= True).pack())])
    menu = buttons
    return InlineKeyboardMarkup(inline_keyboard=menu)

async def create_menu_sites():
    tg_db = site_db("info")
    global channel
    channels = await tg_db.get_sites()
    buttons = []  
    used_channels = await return_rss_in_channel(channel)
    for channel2 in used_channels:
        del channels[channel2[1]]
    for channel1 in channels:
        buttons.append([InlineKeyboardButton(text=f"{channels[channel1][0]}", callback_data=TelegramSiteCallback(id=str(ObjectId(channels[channel1][3]))).pack())])
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back= True).pack())])
    
    
    menu = buttons
    return InlineKeyboardMarkup(inline_keyboard=menu)

async def create_menu_enable_channels():
    global channel
    buttons = []  
    used_channels = await return_in_channel_channels(channel)
    for channel1 in used_channels:
        buttons.append([InlineKeyboardButton(text=f"{channel1[1]}", callback_data=TelegramDeleteCallback(id=int(channel1[0])).pack())])
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back= True).pack())])

    menu = buttons
    return InlineKeyboardMarkup(inline_keyboard=menu)

async def create_menu_enable_sites():
    global channel
    buttons = []  
    used_channels = await return_rss_in_channel(channel)
    for channel1 in used_channels:
        buttons.append([InlineKeyboardButton(text=f"{channel1[1]}", callback_data=TelegramSiteDeleteCallback(id=str(ObjectId(channel1[0]))).pack())])
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back= True).pack())])

    menu = buttons
    return InlineKeyboardMarkup(inline_keyboard=menu)

async def create_menu_enable_channels_for_work_with_word():
    global channel
    buttons = []  
    used_channels = await return_in_channel_channels(channel)
    for channel1 in used_channels:
        buttons.append([InlineKeyboardButton(text=f"{channel1[1]}", callback_data=TelegramEditCallback(id=int(channel1[0])).pack())])
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back= True).pack())])

    menu = buttons
    return InlineKeyboardMarkup(inline_keyboard=menu)

async def create_menu_enable_sites_for_work_with_word():
    global channel
    buttons = []  
    used_channels = await return_rss_in_channel(channel)
    for channel1 in used_channels:
        buttons.append([InlineKeyboardButton(text=f"{channel1[1]}", callback_data=TelegramEditSiteCallback(id=str(ObjectId(channel1[0]))).pack())])
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back= True).pack())])

    menu = buttons
    return InlineKeyboardMarkup(inline_keyboard=menu)

async def create_text_of_channel(id):
    channels = await return_in_channel_channels(id)
    text = ""
    if channels == []:
        text += "\nTelegram источников для парсинга нет"
    else:
        text += "\nTelegram источники для парсинга:\n"
        for channel in channels:
            text += f"- id: {channel[0]}  @{channel[1].split("/")[-1]}\n"
    sites =  await return_rss_in_channel(id)
    if sites == []:
        text += "\nСайтов для парсинга нет"
    else:
        text += "Сайты для парсинга:\n"
        for site in sites:
        
            text += f"- {site[1]}\n"
    return text
    

@admin_channels_manage_router.callback_query(MyCallback.filter(F.id != None))
async def query_channel(callback_query: CallbackQuery):
    global channel
    channel = callback_query.data.split(":")[1]
    await callback_query.message.edit_text(f"Это меню источник {callback_query.data.split(":")[1]}"+ await create_text_of_channel(callback_query.data.split(":")[1]), reply_markup=await create_menu_channel(callback_query.data.split(":")[1]) )


@admin_channels_manage_router.callback_query(F.data == "reduct_channel")
async def query_channel(callback_query: CallbackQuery):
    global channel
    buttons = [
        [InlineKeyboardButton(text="Добавить источник", callback_data="add_channel")],
        [InlineKeyboardButton(text="Удалить источник", callback_data="delete_channel")],
        [InlineKeyboardButton(text="Управление ключевыми словами", callback_data="change_words_channel")],
        ]
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back=True).pack())])
    
    await callback_query.message.edit_text(text = "Функции управления источниками", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@admin_channels_manage_router.callback_query(F.data == "reduct_site")
async def query_channel(callback_query: CallbackQuery):
    global channel
    buttons = [
        [InlineKeyboardButton(text="Добавить сайт", callback_data="add_site")],
        [InlineKeyboardButton(text="Удалить сайт", callback_data="delete_site")],
        [InlineKeyboardButton(text="Управление ключевыми словами", callback_data="change_words_site")],
        ]
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back=True).pack())])
    
    await callback_query.message.edit_text(text = "Функции управления сайтами", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@admin_channels_manage_router.callback_query(F.data == "add_site")
async def query_channel(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text = "Доступные сайты", reply_markup=await create_menu_sites() )

@admin_channels_manage_router.callback_query(F.data == "add_channel")
async def query_channel(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text = "Доступные каналы", reply_markup=await create_menu_channels() )

@admin_channels_manage_router.callback_query(F.data == "delete_channel")
async def query_channel(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text = "Доступные каналы", reply_markup=await create_menu_enable_channels() )

@admin_channels_manage_router.callback_query(F.data == "delete_site")
async def query_channel(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text = "Доступные сайты", reply_markup=await create_menu_enable_sites() )

@admin_channels_manage_router.callback_query(F.data == "change_words_channel")
async def query_channel(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text = "Доступные каналы", reply_markup=await create_menu_enable_channels_for_work_with_word() )

@admin_channels_manage_router.callback_query(F.data == "change_words_site")
async def query_channel(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text = "Доступные сайты", reply_markup=await create_menu_enable_sites_for_work_with_word() )

@admin_channels_manage_router.callback_query(TelegramSiteCallback.filter(F.id != None and F.id != -1))
async def add_site(callback_query: CallbackQuery):
    global channel
    s_db = site_db("info")
    site = await s_db.get_sites_by_id(ObjectId(callback_query.data.split(":")[1]))
    s_db = site_db(channel)
    await s_db.create_new_sites(site["url"])
    await callback_query.message.edit_text(text = "Доступные сайты", reply_markup=await create_menu_sites() )


@admin_channels_manage_router.callback_query(TelegramDeleteCallback.filter(F.id != None and F.id != -1))
async def del_channel(callback_query: CallbackQuery):
    global channel
    tg_db = telegram_db(channel)
    await tg_db.delete_telegram_channel(int(callback_query.data.split(':')[1]))
    await callback_query.message.edit_text(text = "Доступные каналы", reply_markup=await create_menu_enable_channels() )

@admin_channels_manage_router.callback_query(TelegramSiteDeleteCallback.filter(F.id != None and F.id != -1))
async def del_site(callback_query: CallbackQuery):
    global channel
    s_db = site_db(channel)
    await s_db.delete_sites_id(callback_query.data.split(':')[1])
    
    await callback_query.message.edit_text(text = "Доступные сайты", reply_markup=await create_menu_enable_sites() )


@admin_channels_manage_router.callback_query(TelegramEditCallback.filter(F.id != None))
async def edit_channel(callback_query: CallbackQuery):
    global channel
    tg_db = telegram_db(channel)
    in_channel = dict(await tg_db.get_telegram_channel_by_id(int(callback_query.data.split(':')[1])))
    #await tg_db.delete_telegram_channel(int(callback_query.data.split(':')[1]))
    buttons = [
        [InlineKeyboardButton(text="Добавить плюс слово", callback_data=TelegramWords(id=in_channel["id"], add = True, plus=True).pack())],
        [InlineKeyboardButton(text="Удалить плюс слово", callback_data=TelegramWords(id=in_channel["id"], add = False, plus=True).pack())],
        [InlineKeyboardButton(text="Добавить минус слово", callback_data=TelegramWords(id=in_channel["id"], add = True, plus=False).pack())],
        [InlineKeyboardButton(text="Удалить минус слово", callback_data=TelegramWords(id=in_channel["id"], add = False, plus=False).pack())],
        ]
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back=True).pack())])
    w_db = words_db(channel, int(callback_query.data.split(':')[1]))
    text = f"Вы в источнике {in_channel["link_channel"]}"
    text += "\nПлюс слова:\n"
    for word in await w_db.get_key_words():
        text += f"- {word}\n"
    text += "\nМинус слова:\n"
    for word in await w_db.get_del_words():
        text += f"- {word}\n"
    await callback_query.message.edit_text(text = text, reply_markup= InlineKeyboardMarkup(inline_keyboard=buttons), disable_web_page_preview=True)

@admin_channels_manage_router.callback_query(TelegramEditSiteCallback.filter(F.id != None))
async def edit_site(callback_query: CallbackQuery):
    global channel
    s_db = site_db(channel)
    in_channel = dict(await s_db.get_sites_by_id(ObjectId(callback_query.data.split(':')[1])))
    #await tg_db.delete_telegram_channel(int(callback_query.data.split(':')[1]))
    buttons = [
        [InlineKeyboardButton(text="Добавить плюс слово", callback_data=SitesWords(id=str(in_channel["_id"]), add = True, plus=True).pack())],
        [InlineKeyboardButton(text="Удалить плюс слово", callback_data=SitesWords(id=str(in_channel["_id"]), add = False, plus=True).pack())],
        [InlineKeyboardButton(text="Добавить минус слово", callback_data=SitesWords(id=str(in_channel["_id"]), add = True, plus=False).pack())],
        [InlineKeyboardButton(text="Удалить минус слово", callback_data=SitesWords(id=str(in_channel["_id"]), add = False, plus=False).pack())],
        ]
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back=True).pack())])
    w_db = sites_words_db(channel, callback_query.data.split(':')[1])
    text = f"Вы в сайте {in_channel["url"]}"
    text += "\nПлюс слова:\n"
    for word in await w_db.get_key_words():
        text += f"- {word}\n"
    text += "\nМинус слова:\n"
    for word in await w_db.get_del_words():
        text += f"- {word}\n"
    await callback_query.message.edit_text(text = text, reply_markup= InlineKeyboardMarkup(inline_keyboard=buttons), disable_web_page_preview=True)

class AddWords(StatesGroup):
    words = State()
    add = State()
    plus = State()
    id = State()


    texts = {
        'AddWords:words': 'Введите id канала заново',
        'AddWords:add': 'Введите id канала заново',
        'AddWords:plus': 'Введите id канала заново',
    }

@admin_channels_manage_router.callback_query(TelegramWords.filter(F.id != None))
async def add_plus_word(callback_query: CallbackQuery, state:FSMContext):
    await callback_query.message.answer("Введите слово или слова через пробел \n Для отмены нажмите на кнопку", reply_markup=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text ="/отмена"),
        ]
    
    ],
    resize_keyboard=True,
))
    
    await state.set_state(AddWords.words)
    await state.update_data(id = callback_query.data.split(":")[1])

    await state.update_data(add = int(callback_query.data.split(":")[2]) == 1)
    await state.update_data(plus = int(callback_query.data.split(":")[3]) == 1)
   # await state.update_data(id = .)


@admin_channels_manage_router.message(StateFilter(AddWords.words), F.text)
async def source(message: types.Message, state: FSMContext):
    if message.text == " ":
        await message.answer("Слова фильтрации должны состоять хотя бы из одного слова")
        return
    await state.update_data(words = message.text.lower().split(" "))
    data = await state.get_data()
    global channel
    w_db = words_db(channel, int(data['id']))
    if data['add'] == True and data['plus'] == True:
        await w_db.add_key_words(list(data['words'])) 
    elif data['add'] == False and data['plus'] == True:
        await w_db.delete_key_words(list(data['words'])) 
    elif data['add'] == True and data['plus'] == False:
        await w_db.add_bad_words(list(data['words'])) 
    else:
        await w_db.delete_bad_words(list(data['words'])) 
    await message.answer(text = "Успешно", reply_markup=reply.manage_channels_markup)
    await state.clear()
    tg_db = telegram_db(channel)
    in_channel = dict(await tg_db.get_telegram_channel_by_id(int(data['id'])))
    #await tg_db.delete_telegram_channel(int(callback_query.data.split(':')[1]))
    buttons = [
        [InlineKeyboardButton(text="Добавить плюс слово", callback_data=TelegramWords(id=in_channel["id"], add = True, plus=True).pack())],
        [InlineKeyboardButton(text="Удалить плюс слово", callback_data=TelegramWords(id=in_channel["id"], add = False, plus=True).pack())],
        [InlineKeyboardButton(text="Добавить минус слово", callback_data=TelegramWords(id=in_channel["id"], add = True, plus=False).pack())],
        [InlineKeyboardButton(text="Удалить минус слово", callback_data=TelegramWords(id=in_channel["id"], add = False, plus=False).pack())],
        ]
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back=True).pack())])
    text = f"Вы в источнике {in_channel["link_channel"]}"
    text += "\nПлюс слова:\n"
    for word in await w_db.get_key_words():
        text += f"- {word}\n"
    text += "\nМинус слова:\n"
    for word in await w_db.get_del_words():
        text += f"- {word}\n"
    await message.answer(text = text, reply_markup= InlineKeyboardMarkup(inline_keyboard=buttons), disable_web_page_preview=True)



class AddSitesWords(StatesGroup):
    words = State()
    add = State()
    plus = State()
    id = State()


    texts = {
        'AddSitesWords:words': 'Введите id канала заново',
        'AddSitesWords:add': 'Введите id канала заново',
        'AddSitesWords:plus': 'Введите id канала заново',
    }

@admin_channels_manage_router.callback_query(SitesWords.filter(F.id != None))
async def add_plus_word(callback_query: CallbackQuery, state:FSMContext):
    await callback_query.message.answer("Введите слово или слова через пробел \n Для отмены нажмите на кнопку", reply_markup=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text ="/отмена"),
        ]
    
    ],
    resize_keyboard=True,
))
    
    await state.set_state(AddSitesWords.words)
    await state.update_data(id = callback_query.data.split(":")[1])

    await state.update_data(add = int(callback_query.data.split(":")[2]) == 1)
    await state.update_data(plus = int(callback_query.data.split(":")[3]) == 1)
   # await state.update_data(id = .)


@admin_channels_manage_router.message(StateFilter(AddSitesWords.words), F.text)
async def source(message: types.Message, state: FSMContext):
    if message.text == " ":
        await message.answer("Слова фильтрации должны состоять хотя бы из одного слова")
        return
    await state.update_data(words = message.text.lower().split(" "))
    data = await state.get_data()
    global channel
    w_db = sites_words_db(channel, data['id'])
    if data['add'] == True and data['plus'] == True:
        await w_db.add_key_words(list(data['words'])) 
    elif data['add'] == False and data['plus'] == True:
        await w_db.delete_key_words(list(data['words'])) 
    elif data['add'] == True and data['plus'] == False:
        await w_db.add_bad_words(list(data['words'])) 
    else:
        await w_db.delete_bad_words(list(data['words'])) 
    await message.answer(text = "Успешно", reply_markup=reply.manage_channels_markup)
    await state.clear()
    s_db = site_db(channel)
    in_channel = dict(await s_db.get_sites_by_id(ObjectId(data['id'])))
    #await tg_db.delete_telegram_channel(int(callback_query.data.split(':')[1]))
    buttons = [
        [InlineKeyboardButton(text="Добавить плюс слово", callback_data=SitesWords(id=str(in_channel["_id"]), add = True, plus=True).pack())],
        [InlineKeyboardButton(text="Удалить плюс слово", callback_data=SitesWords(id=str(in_channel["_id"]), add = False, plus=True).pack())],
        [InlineKeyboardButton(text="Добавить минус слово", callback_data=SitesWords(id=str(in_channel["_id"]), add = True, plus=False).pack())],
        [InlineKeyboardButton(text="Удалить минус слово", callback_data=SitesWords(id=str(in_channel["_id"]), add = False, plus=False).pack())],
        ]
    buttons.append( [InlineKeyboardButton(text="Назад", callback_data=SettingsCallback(id=channel, back=True).pack())])
    text = f"Вы в сайте {in_channel["url"]}"
    text += "\nПлюс слова:\n"
    for word in await w_db.get_key_words():
        text += f"- {word}\n"
    text += "\nМинус слова:\n"
    for word in await w_db.get_del_words():
        text += f"- {word}\n"
    await message.answer(text = text, reply_markup= InlineKeyboardMarkup(inline_keyboard=buttons), disable_web_page_preview=True)
    

@admin_channels_manage_router.callback_query(TelegramCallback.filter(F.id != None and F.id != -1))
async def add_channel2(callback_query: CallbackQuery):
    tg_db = telegram_db("info")
    channels = await tg_db.get_telegramm_channels()
    global channel
    tg_db = telegram_db(channel)
    await tg_db.add_telegram_channel(channels[int(callback_query.data.split(":")[1])][0], int(callback_query.data.split(":")[1]))
    await callback_query.message.edit_text(text = "Доступные каналы", reply_markup=await create_menu_channels() )


@admin_channels_manage_router.callback_query(F.data == "main")
async def source(callback_query: CallbackQuery):
    await callback_query.message.edit_text(await create_text(), reply_markup=await create_menu())

@admin_channels_manage_router.message(StateFilter(None), F.text.lower() == "управление каналами")
async def source(message: types.Message):
    await message.answer(await create_text(), reply_markup=await create_menu())
    await message.answer("Перед вами открылось меню в которое входит: удаления, добавления.", reply_markup=reply.manage_channels_markup)


@admin_channels_manage_router.callback_query(SettingsCallback.filter(F.back == True))
async def query_change_date(callback_query: CallbackQuery):
    await callback_query.message.edit_text(f"Это меню канала {callback_query.data.split(":")[1]}"+ await create_text_of_channel(callback_query.data.split(":")[1]), reply_markup=await create_menu_channel(callback_query.data.split(":")[1]) )

class AddChannel(StatesGroup):
    id = State()
    name = State()
    texts = {
        'AddChannel:id': 'Введите id канала заново',
        'AddChannel:name': 'Введите name канала заново',
    }

class DeleteChannel(StatesGroup):
    id = State()
    texts = {
        'DeleteChannel:id': 'Введите id канала заново',
    }



@admin_channels_manage_router.message(StateFilter(None), F.text.lower() == "добавить канал")
async def add_channel1(message: types.Message, state: FSMContext):
    await message.answer("Введите id канала", reply_markup= ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text ="/отмена"),] ],resize_keyboard=True))
    await state.set_state(AddChannel.id)
    
@admin_channels_manage_router.message(StateFilter(AddChannel.id), F.text.replace("-","").isdigit())
async def source(message: types.Message, state: FSMContext):
    await state.update_data(id = message.text.lower())
    await state.set_state(AddChannel.name)
    await message.answer("Введите название канала", reply_markup= ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text ="/отмена"),] ],resize_keyboard=True))
    
@admin_channels_manage_router.message(StateFilter(AddChannel.name), F.text !="")
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name = message.text)
    data = await state.get_data()
    await add_channel(data['id'], data['name'])
    await state.clear()
    await message.answer("Успешно", reply_markup=reply.manage_channels_markup)
    

@admin_channels_manage_router.message(StateFilter(None), F.text.lower() == "удаление канала")
async def delete_channel1(message: types.Message, state: FSMContext):
    await message.answer("Введите id канала", reply_markup= ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text ="/отмена"),] ],resize_keyboard=True))
    await state.set_state(DeleteChannel.id)

@admin_channels_manage_router.message(StateFilter(DeleteChannel.id), F.text)
async def source(message: types.Message, state: FSMContext):
    await delete_channel(message.text.lower())
    await state.clear()
    await message.answer("Успешно", reply_markup=reply.manage_channels_markup)

        