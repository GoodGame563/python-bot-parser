from aiogram.types import KeyboardButtonPollType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


main_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Фильтрация постов источника"),
        ],
        [
            KeyboardButton(text = "Настройки"),
        ],
        [
            KeyboardButton(text = "Каналы"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

telegram_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Управление каналами"),
            KeyboardButton(text = "Управление источниками"),
        ],
        [
           # KeyboardButton(text = "Общие настройки"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

del_kbd = ReplyKeyboardRemove()

manage_sources_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Добавить источник для парсинга"),
        ],
        [
            KeyboardButton(text ="Редактировать источник для парсинга"),
        ],    
        [ 
            KeyboardButton(text ="Удаление источника для парсинга")
        ],
        [
            KeyboardButton(text = "Назад"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

manage_sites_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Добавить сайт для парсинга"),
        ],
        [
           # KeyboardButton(text ="Редактировать источник для парсинга"),
        ],    
        [ 
            KeyboardButton(text ="Удаление сайта для парсинга")
        ],
        [
            KeyboardButton(text = "Назад"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)
manage_channels_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Добавить канал"),
        ],
        [
            #KeyboardButton(text ="Редактировать канал"),
        ],    
        [ 
            KeyboardButton(text ="Удаление канала")
        ],
        [
            KeyboardButton(text = "Назад"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

sites_or_channels_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Сайты"),
        ],
        [
            #KeyboardButton(text ="Редактировать канал"),
        ],    
        [ 
            KeyboardButton(text ="Каналы")
        ],
        [
            KeyboardButton(text = "Назад"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)


time_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
           KeyboardButton(text="Добавить расписание работы бота"), 
        ],
        [
            KeyboardButton(text="Включение/отключение функций бота"),
        ],
        [
            KeyboardButton(text = "Назад"),
        ],
    ],
    resize_keyboard=True,
    
)

raspisanie_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Бот будет работать с"),
            KeyboardButton(text="Бот будет рабоать до"),
        ],
        [
            KeyboardButton(text = "Назад"),
        ],
        
    ],
    resize_keyboard=True,
)


filter_post_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Добавление ключевых слов для фильтра"),
        ],
        [
            KeyboardButton(text ="Редактирование ключевого слова из фильтра"),
        ],    
        [ 
            KeyboardButton(text ="Удаление ключевого слова из фильтра"),
        ],
        [
            KeyboardButton(text = "Назад")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

edit_post_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text ="Парсить статьи вместе с картинками"),
        ],    
        [ 
            KeyboardButton(text ="Оставлять гипер ссылки"),
        ],
        [
            KeyboardButton(text = "Назад"),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

razdel_tg_sait_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Телеграм каналы"),
            KeyboardButton(text="Сайты"),
        ],
        [
            KeyboardButton(text = "Назад"),
        ],
        
    ],
    resize_keyboard=True,
)

dop_vozmoc_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="С какого момента парсить?"),
        ],
        [
            KeyboardButton(text = "Назад"),
        ],
        
    ],
    resize_keyboard=True,
)
