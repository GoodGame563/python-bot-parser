from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, or_f, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F, types, Router

from kbds import reply
from data.telegram_channel_db import *
from logs.loging import log_admin_bot
from data.key_words_db import *
from handlers.filters import ChatTypeFilter, IsAdmin

admin_key_words_manage_router = Router()
admin_key_words_manage_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_key_words_manage_router.message(StateFilter(None), F.text.lower() == "фильтрация постов источника")
async def filter_key_words(message: types.Message):
    await message.answer("Перед вами открылось меню для редактирвания в которое входит добавление источников для парсинга.", reply_markup=reply.filter_post_markup)


@admin_key_words_manage_router.message(StateFilter('*'), Command("отмена"))
@admin_key_words_manage_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=reply.main_menu_markup)


class AddWords(StatesGroup):
    words = State()

    texts = {
        'AddWords:words': 'Введите id канала заново'
    }

@admin_key_words_manage_router.message(StateFilter(None), F.text.lower() == "добавление ключевых слов для фильтра")
async def add_key_words_router(message: types.Message, state: FSMContext):
    await message.answer("Напишите ключевые слова/слово через пробел", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddWords.words)

@admin_key_words_manage_router.message(AddWords.words, F.text)
async def add_words(message: types.Message, state: FSMContext):
    if message.text == " ":
        await message.answer("Слова фильтрации должны состоять хотя бы из одного слова")
        return
    await state.update_data(words = message.text.lower().split(" "))
    data = await state.get_data()
    add_key_words(data['words'])
    await state.clear()
    await message.answer("Ключевые слова добавлены", reply_markup=reply.filter_post_markup)

@admin_key_words_manage_router.message(AddWords.words)
async def add_key_words_router2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")


class ReductWords(StatesGroup):
    word = State()
    new_word = State()

    texts = {
        'ReductWords:word': 'Введите id канала заново',
        'ReductWords:new_word': 'Введите id канала заново'
    }

@admin_key_words_manage_router.message(StateFilter(None), F.text.lower() == "редактирование ключевого слова из фильтра")
async def reduct_key_words(message: types.Message, state: FSMContext):
    key_words = await get_key_words()
    if len(key_words) == 0 or key_words is None:
        await message.answer("Нет ключевых слов для редактирования")
        return
    key_words_to_str = "".join ([f"- {key_words[id_key]}\n" for id_key in key_words])
    text = "Слова используемые для парсинга:\n" + key_words_to_str
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Введите слово ", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ReductWords.word)

@admin_key_words_manage_router.message(StateFilter(ReductWords.word), F.text)
async def reduct_target_word(message: types.Message, state: FSMContext):
    if message.text == " ":
        await message.answer("Слово фильтрации должно состоять хотя бы из одного слова")
        return
    key_words = await get_key_words()
    if message.text.lower() in key_words.values():
        await message.answer("Введите новое слово", reply_markup=types.ReplyKeyboardRemove())
        await state.update_data(word = message.text.lower())
        await state.set_state(ReductWords.new_word)
    else:
        await message.answer("Введите существующие слово", reply_markup=types.ReplyKeyboardRemove())
        return
    
@admin_key_words_manage_router.message(StateFilter(ReductWords.word))
async def reduct_target_word1(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")

@admin_key_words_manage_router.message(StateFilter(ReductWords.new_word), F.text)
async def reduct_target_word_new_word(message: types.Message, state: FSMContext):
    if message.text == " ":
        await message.answer("Слово фильтрации должно состоять хотя бы из одного слова")
        return
    await state.set_data(new_word = message.text().lower())
    data = await state.get_data()
    await state.clear()
    await reduct_key_word(data['word'], data['new_word'])
    await message.answer("Ключевое слово изменено", reply_markup=reply.filter_post_markup)
    
@admin_key_words_manage_router.message(StateFilter(ReductWords.new_word))
async def reduct_target_word_new_word1(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")


class DeleteWords(StatesGroup):
    words = State()
    texts = {
        'DeleteWords:words': 'Введите id канала заново'
    }

@admin_key_words_manage_router.message(StateFilter(None), F.text.lower() == "удаление ключевого слова из фильтра")
async def delete_key_words_router(message: types.Message, state: FSMContext):
    key_words = await get_key_words()
    if len(key_words) == 0 or key_words is None:
        await message.answer("Нет ключевых слов для удаления")
        return
    key_words_to_str = "".join ([f"- {key_words[id_key]}\n" for id_key in key_words])
    text = "Слова используемые для парсинга:\n" + key_words_to_str
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Введите слово/слова для удаления ", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(DeleteWords.words)

@admin_key_words_manage_router.message(StateFilter(DeleteWords.words), F.text)
async def delete_key_word(message: types.Message, state: FSMContext):
    if message.text == " ":
        await message.answer("Слова фильтрации должны состоять хотя бы из одного слова")
        return
    await state.update_data(words = message.text.lower().split(" "))
    data = await state.get_data()
    await delete_key_words(data['words'])
    await state.clear()
    await message.answer("Ключевые слова удалены", reply_markup=reply.filter_post_markup)

@admin_key_words_manage_router.message(StateFilter(DeleteWords.words))
async def delete_key_word1(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные")
