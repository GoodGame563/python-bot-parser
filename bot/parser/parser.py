from parser.parser_functions import parse # библиотека этого парсера
from dotenv import load_dotenv
from os import environ
import os
import sys
from telethon import TelegramClient, events, connection
from logs.loging import log_parser_bot
sys.path.append(os.path.join(os.getcwd(), '..'))

load_dotenv()

api_id = environ.get('API_ID')
api_hash = environ.get('API_HASH')
log = log_parser_bot()

if api_id is None and api_hash is None:
    assert ()
else:
    log.send_info("script started")  # сообщение о начале работы в лог

async def parse_channel(url_list:list ):
    async with TelegramClient('new', api_id, api_hash, device_model='Samsung Galaxy S20 FE, running Android 13', system_version='4.16.30-vxCUSTOM', app_version='1.0.1') as tc:
        for url in url_list:
            try:
                log.send_info(f"parsing channel {url}")
                mem = await parse(tc, url)
                for er in mem:
                    log.send_debug(f"{er}")
                log.send_info("parsing done successfully")
                pass
            except Exception as ex: 
                log.send_critical(f"critical error {ex}")
            finally: 
                log.send_debug('parsing stop')
        tc.disconnect()
