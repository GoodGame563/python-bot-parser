from dotenv import load_dotenv
import os
import sys
import asyncio
sys.path.append(os.path.join(os.getcwd(), '..'))
from logs.loging import log_admin_bot
from data.base_connection_db import check_exist_database_if_create
from data.telegram_channel_db import *
import parser.parser


load_dotenv()

async def start_parsing():
    check_exist_database_if_create()
    all_channels = get_telegramm_channels()
    if all_channels is None:
        log_admin_bot().send_critical("Could not connect to database")
        return None
    channel = list()
    for key in all_channels:
        channel.append(all_channels[key][0])
    if channel != {}:
        pass
        #await parser.parser.parse_channel(channel)
