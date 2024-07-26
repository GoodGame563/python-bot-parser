from aiogram.filters import Filter
from aiogram.filters.callback_data import CallbackData
from aiogram import Bot, types


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types
    

class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in bot.my_admins_list
    
class TelegramCallback(CallbackData, prefix ="tg_add"):
    id:int

class TelegramDeleteCallback(CallbackData, prefix ="tg_delete"):
    id:int

class TelegramEditCallback(CallbackData, prefix ="tg_edit"):
    id:int
class TelegramSiteCallback(CallbackData, prefix ="site_add"):
    id:str
class TelegramEditSiteCallback(CallbackData, prefix ="site_edit"):
    id:str
class TelegramSiteDeleteCallback(CallbackData, prefix ="site_delete"):
    id:str
class TelegramWords(CallbackData, prefix ="tg_words"):
    id:int
    add:bool
    plus:bool

class SitesWords(CallbackData, prefix ="sites_words"):
    id:str
    add:bool
    plus:bool


class SettingsCallback(CallbackData, prefix ="settings"):
    id:int
    back:bool