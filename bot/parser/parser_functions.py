from glob import glob
import asyncio
from telethon.tl.types import MessageEntityTextUrl
from dateutil.relativedelta import relativedelta  # pip3 install python-dateutil

import datetime
import os
import sys
import shutil

sys.path.append(os.path.join(os.getcwd(), '..'))
from data.telegram_channel_db import create_new_telegram_channel_parsing, return_data_last_changed_telegram_channel, add_image_to_telegram_channel, check_post_exist_in_telegram_channel, update_date_telegram_channel 
from data.db import get_key_words
from parser.minio_function import add_file
from logs.loging import log_parser_bot


main_folder = "record"

def get_text_from_filters(text):
    words = get_key_words()
    if words is None:
        return None
    if len(words) == 0: 
        return True
    ad_delete = os.environ.get('DELETE_AD_POST')
    if ad_delete is None or ad_delete == "True":
        if "erid" in text.lower():
            return False
    for id_word in words:
        if words[id_word] in text.lower():
            log_parser_bot().send_debug(f"слово {words[id_word]}")
            return True
    return False



async def get_channel_id(client, link):  # получение ID канала
    m = await client.get_messages(link, limit=1)
    channel_id = m[0].peer_id.channel_id
    return str(channel_id)


def clearify_text(msg):  # очищение текста от символов гиперссылки
    text = msg.message
    
    find_int_dog = text.find('@')
    if find_int_dog != -1:
        print("Found")
        find_int_end_word = text.find(' ',  find_int_dog)
        text = text[:find_int_dog-1] + text[find_int_end_word+1:]
    find_int_cross = text.find('#')
    if find_int_cross!= -1:
        find_int_end_word = text.find(' ', find_int_cross)
        text = text[:find_int_cross] + text[find_int_end_word+1:]
    return text

async def get_image(client, msg, channel_name, directory_name):
    if msg.media:
        data = await client.download_media(msg, f"{main_folder}/{channel_name}/{directory_name}")
       
        return f"{channel_name}/{msg.id}.{data.split(".")[1]}"


def find_last_parsed_date(id:int): 
    oldest = datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    temp = oldest
    oldest = return_data_last_changed_telegram_channel(int(id))
    if oldest is None:
        return None
    if temp == oldest:
        oldest = datetime.datetime.now() - relativedelta(days=1)  # если сообщений нет, офсет устанавливается на                                                   # три месяца от текущей даты
    return oldest


async def parse(client, url):
    err = []  
    channel_id = await get_channel_id(client, url)  
    oldest = find_last_parsed_date(int(channel_id))
    if oldest is None: 
        return []
    oldest += relativedelta(seconds=1) 
    async for message in client.iter_messages(url, reverse=True, offset_date=oldest):
        await asyncio.sleep(0.5)
        try:
            directory_name = str(message.id) 
            if message.message:
                if (get_text_from_filters(message.message)):
                    create_new_telegram_channel_parsing(channel_id, message.date, clearify_text(message), message.id)
                else:
                    update_date_telegram_channel(channel_id, message.date)
            if message.media:
                if(check_post_exist_in_telegram_channel(channel_id, datetime.datetime.strptime(message.date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))):
                    url_path = await get_image(client, message, channel_id, directory_name)
                    if (add_image_to_telegram_channel(channel_id, url_path, datetime.datetime.strptime(message.date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))):
                        #print(os.path.getsize(f"{url_path}"))
                        add_file(url_path.split('/')[1], channel_id, f"{main_folder}/{url_path}")
                else:
                    update_date_telegram_channel(channel_id, message.date)
        except Exception as passing: 
            err.append(passing)
            continue
        if (os.path.isdir(f"{main_folder}/{channel_id}")): 
            shutil.rmtree(f"{main_folder}/{channel_id}")
    return err