from aiogram.types import KeyboardButtonPollType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


main_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Управление источниками"),
            KeyboardButton(text = "Фильтрация постов источника"),
        ],
        [
            KeyboardButton(text = "Редактирование поста"),
            KeyboardButton(text = "Расписание работы"),
        ],
        [
            KeyboardButton(text = "Дополнительные возможности"),
        ]
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
            KeyboardButton(text ="Удаление всего списка для парсинга")
        ],
        [
            KeyboardButton(text = "back"),
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
            KeyboardButton(text="Выключить бота"),
        ],
        [
            KeyboardButton(text = "back"),
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
            KeyboardButton(text = "back"),
        ],
        
    ],
    resize_keyboard=True,
)


filter_post_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Введите ключевые слова для фильтра"),
        ],
        [
            KeyboardButton(text ="Редактировать ключевые слова  для фильтра"),
        ],    
        [ 
            KeyboardButton(text ="Удаление всех ключевых слов из фильтра"),
        ],
        [
            KeyboardButton(text = "back")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

edit_post_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Принятие или отклонение поста"),
        ],
        [
            KeyboardButton(text ="Парсить статьи вместе с картинками"),
        ],    
        [ 
            KeyboardButton(text ="Оставлять гипер ссылки"),
        ],
        [
            KeyboardButton(text = "back"),
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
            KeyboardButton(text = "back"),
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
            KeyboardButton(text = "back"),
        ],
        
    ],
    resize_keyboard=True,
)