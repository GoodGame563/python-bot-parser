import asyncio 
import os
import sys


sys.path.append(os.path.join(os.getcwd(), '..'))
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, StateFilter



from work_to_parse import start_parsing
from kbds import reply
from dotenv import load_dotenv
from data.telegram_channel_db import *
from data.settings_db import *
from work_to_post_in_channel import print_post
from logs.loging import log_admin_bot
from handlers.sources_router import admin_source_manage_router
from handlers.key_words_router import admin_key_words_manage_router
from handlers.settings_router import admin_settings_manage_router
from handlers.user_group import user_group_router
from handlers.admin_router import admin_router
from data.base_connection_db import *
from data.minio_function import check_backet_exists


load_dotenv()


bot_token = os.environ.get('BOT_TOKEN')
if bot_token is None or bot_token == '':
    log_admin_bot().send_critical('Bot token missing')
    assert ()
else:
    log_admin_bot().send_info('Bot token is set')


bot = Bot(token=bot_token)
bot.my_admins_list = []
dp = Dispatcher()

dp.include_routers(user_group_router)
dp.include_routers(admin_source_manage_router)
dp.include_routers(admin_key_words_manage_router)
dp.include_router(admin_settings_manage_router)
dp.include_router(admin_router)



async def main():
    while True:
        if get_url_connection() is None:
            log_admin_bot().send_critical("Нет соединения с базой данных")
            log_admin_bot().send_info("Попытка подсоединения к базе данных")
            await asyncio.sleep(60)
            return
        break
    await check_backet_exists()
    await set_basic_parameters()
    await get_all_settings()
    task1 = asyncio.create_task(dp.start_polling(bot))
    task2 = asyncio.create_task(start_parsing())
    task3 = asyncio.create_task(print_post(bot))
    log_admin_bot().send_info("bot started")
    print("Bot started")

    await asyncio.gather(task1, task2, task3)

    

asyncio.run(main()) 