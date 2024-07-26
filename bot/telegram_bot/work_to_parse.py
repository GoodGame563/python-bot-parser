from dotenv import load_dotenv
import os
import sys
import asyncio
sys.path.append(os.path.join(os.getcwd(), '..'))
from logs.loging import log_admin_bot, log_parser_bot
from data.telegram_channel_db import telegram_db
from data.settings_db import *
from data.channels_db import return_channels
from parser.parser import parse_channel


load_dotenv()

async def start_parsing():
    while True:
        for channel in await return_channels():
            set_db = setting_db(channel)
            settings = await set_db.get_all_settings()
            if not (settings).get("parser"):
                log_parser_bot().send_info("Parser is stopped")
                await asyncio.sleep(60)
                continue
            log_admin_bot().send_info("Parser is running")
            tg_db = telegram_db(channel)
            all_channels = await tg_db.get_telegramm_channels()
            if all_channels is not None:
                await parse_channel(all_channels, channel)
        await asyncio.sleep(305)
