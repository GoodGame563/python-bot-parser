from parser.parser_functions import parse 
from dotenv import load_dotenv
from os import environ
import os
import sys
from telethon import TelegramClient
from logs.loging import log_parser_bot
sys.path.append(os.path.join(os.getcwd(), '..'))

load_dotenv()

api_id = environ.get('API_ID')
api_hash = environ.get('API_HASH')
log = log_parser_bot()

tc = TelegramClient('../session/new', api_id, api_hash, device_model='Samsung Galaxy S21, running Android 15', system_version='4.16.30-vxCUSTOM', app_version='1.0.2')

if api_id is None and api_hash is None:
    assert ()
else:
    log.send_info("script started") 

async def parse_channel(channel_dict:dict, channel_name:str ):
    if not tc.is_connected():
        await tc.connect()
        await tc.start()
    for id in channel_dict:
        # try:
            log.send_info(f"parsing channel {channel_dict[id][0]}")
            mem = []
            #print(channel_name, tc, channel_dict[id][0], channel_dict[id][3], channel_dict[id][4])
            mem = await parse(channel_name, tc, channel_dict[id][0], channel_dict[id][3], channel_dict[id][4])
            for er in mem:
                log.send_debug(f"{er}")
            log.send_info("parsing done successfully")
        # except Exception as ex: 
        #     log.send_critical(f"critical error {ex}")
        # finally: 
        #     log.send_debug('parsing stop')
