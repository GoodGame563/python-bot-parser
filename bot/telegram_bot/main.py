import asyncio 
import os
import sys
import time

sys.path.append(os.path.join(os.getcwd(), '..'))
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, StateFilter



from work_to_parse import start_parsing
from kbds import reply
from dotenv import load_dotenv
from data.telegram_channel_db import telegram_db
from data.settings_db import *
from work_to_post_in_channel import print_post
from logs.loging import log_admin_bot
from handlers.sources_router import admin_source_manage_router
from handlers.key_words_router import admin_key_words_manage_router
from handlers.settings_router import admin_settings_manage_router
from handlers.user_group import user_group_router, create_admin
from handlers.admin_router import admin_router
from handlers.channels_router import admin_channels_manage_router
from data.channels_db import check_channels_exist, return_channels
from data.base_connection_db import *
from data.minio_function import check_backet_exists
from web_parser.rss_parser import rss_parser


load_dotenv()
page  = 0
step = 15

bot_token = os.environ.get('BOT_TOKEN')

bot_token = os.environ.get('BOT_TOKEN')
if bot_token is None or bot_token == '':
    log_admin_bot().send_critical('Bot token missing')
    assert()
else:
    log_admin_bot().send_info('Bot token is set')


admin_chat_id = os.environ.get('ADMIN_CHAT_ID')
if admin_chat_id is None or admin_chat_id == '':
    log_admin_bot().send_critical('Admin chat is missing')
    assert()
else:
    log_admin_bot().send_info('Admin chat is enabled')


bot = Bot(token=bot_token)
bot.my_admins_list = []
dp = Dispatcher()
dp.include_routers(user_group_router)
dp.include_routers(admin_source_manage_router)
dp.include_routers(admin_key_words_manage_router)
dp.include_router(admin_settings_manage_router)
dp.include_router(admin_router)
dp.include_router(admin_channels_manage_router)

    
async def send_message(chat_id, message):
    await bot.send_message(chat_id=chat_id, message=message)

async def check_minio():
    while True:
        minio_bucket_name = os.environ.get('MINIO_BUCKET_NAME')
        if minio_bucket_name is None or minio_bucket_name == '':
            log_admin_bot().send_critical('Minio bucket name not found')
            await asyncio.sleep(60)
        else:
            log_admin_bot().send_info('Minio bucket name found: %s' % minio_bucket_name)
            break
    await check_backet_exists()

async def check_mongo():
    await check_exist_database_if_create()
    

async def check_all_for_work():
    print('Checking all for work')
    while True:
        if get_url_connection() is None:
            print('Database connection is not available')
            log_admin_bot().send_critical("Нет соединения с базой данных")
            log_admin_bot().send_info("Попытка подсоединения к базе данных")
            time.sleep(10)
        break
    await check_mongo()

    await check_minio()

    print("All done")
    

async def main():
    await check_all_for_work()
    task1 = asyncio.create_task(dp.start_polling(bot))
    task2 = asyncio.create_task(start_parsing())
    task3 = asyncio.create_task(print_post(bot))
    task4 = asyncio.create_task(rss_parser())
    await create_admin(bot)
    log_admin_bot().send_info("bot started")
    print("Bot started")
    await asyncio.gather(task1, task2, task3, task4)

    

asyncio.run(main()) 