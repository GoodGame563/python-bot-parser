from string import punctuation

from aiogram import F, Bot, types, Router
from aiogram.filters import Command
from aiogram.filters import Filter

from handlers.filters import ChatTypeFilter


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))


@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    admins_list = await bot.get_chat_administrators(-1002022330460)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))
