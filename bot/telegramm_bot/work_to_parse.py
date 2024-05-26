from dotenv import load_dotenv
import os
import sys
import asyncio
sys.path.append(os.path.join(os.getcwd(), '..'))
from logs.loging import log_admin_bot, log_parser_bot
from data.telegram_channel_db import *
from data.settings_db import get_all_settings
import parser.parser


load_dotenv()

async def start_parsing():
    while True:
        settings = await get_all_settings()
        if not (settings).get("parser"):
            log_parser_bot().send_info("Parser is stopped")
            await asyncio.sleep(60)
            continue
        log_admin_bot().send_info("Parser is running")
        all_channels = await get_telegramm_channels()
        if all_channels is None:
            log_parser_bot().send_critical("Could not connect to database")
            return None
        channel = list()
        for key in all_channels:
            channel.append(all_channels[key][0])
        if channel != {}:
            await parser.parser.parse_channel(channel)
        await asyncio.sleep(305)
