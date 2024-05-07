from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Управление источниками"),
            KeyboardButton(text = "Фильтрация постов источника"),
        ],
        [
            KeyboardButton(text = "Редактирование поста"),
            KeyboardButton(text = "Расписание работы")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

manage_sources_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Редактирование"),
            KeyboardButton(text ="Добавление"),
            KeyboardButton(text ="Удаление")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

filter_posts_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Добавление"),
            KeyboardButton(text = "Редактирование"),
            KeyboardButton(text = "Удаление")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)

schedule_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Отключить режим"),
            KeyboardButton(text = "Выставить время работы")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Что вас интересует?"
)