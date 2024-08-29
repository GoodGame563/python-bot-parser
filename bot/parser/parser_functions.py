import asyncio
import telethon.tl.custom
from telethon.tl.types import MessageMediaWebPage, MessageMediaPhoto, MessageEntityTextUrl
from dateutil.relativedelta import relativedelta  

import datetime
import os
import sys
import shutil
from io import BytesIO

sys.path.append(os.path.join(os.getcwd(), '..'))
from data.telegram_channel_db import telegram_db
from data.minio_function import add_file
from logs.loging import log_parser_bot


main_folder = "record"

async def get_text_from_filters(message: telethon.tl.custom.message.Message, key_words, bad_words):
    for ent, _ in message.get_entities_text():
        if(type(ent) is MessageEntityTextUrl):
            message.message = message.message[:ent.offset]+message.message[ent.offset+ent.length:]

    text = message.message
    for bad in bad_words:
        if bad in text.lower():
            return False
        
    if len(key_words) == 0: 
        return True
    for good in key_words:
        if good in text.lower():
            log_parser_bot().send_debug(f"слово {good}")
            return True
    return False



async def get_channel_id(client, link): 
    m = await client.get_messages(link, limit=1)
    channel_id = m[0].peer_id.channel_id
    return str(channel_id)


def clearify_text(msg: telethon.tl.custom.message.Message):  
    
    text = msg.message
    text += "     "
    
    find_int_dog = text.find('@')
    if find_int_dog != -1:
        find_int_end_word = text.find(' ',  find_int_dog)
        if find_int_end_word == -1:
            find_int_end_word = text.find('\n',  find_int_dog)
        text = text[:find_int_dog-1] + text[find_int_end_word+1:]
    cross_count = 0
    find_int_cross = text.find('#')
    #print(find_int_cross)
    if find_int_cross!= -1:
        find_int_end_word = text.find(' ', find_int_cross)
        if find_int_end_word == -1:
            find_int_end_word = text.find('\n',  find_int_dog)
        text = text[:find_int_cross] + text[find_int_end_word+1:]
        text = text.replace("*","").replace("$","")
    return text

async def get_image(client, msg, channel_name = None):
    if msg.media:
        if channel_name is None:
            data = await client.download_media(msg, bytes)    
            return BytesIO(data)
        else: 
            if type(msg.media) == MessageMediaWebPage or type(msg.media) == MessageMediaPhoto:
                #print(type(msg.media))
                return f"{channel_name}/{msg.id}.jpg"
            else:
                return f"{channel_name}/{msg.id}.mp4"



async def find_last_parsed_date(channel, id:int): 
    oldest = datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    temp = oldest
    tg_db = telegram_db(channel)
    oldest = await tg_db.return_data_last_changed_telegram_channel(int(id))
    if oldest is None:
        return None
    if temp == oldest:
        oldest = datetime.datetime.now() - relativedelta(days=1)  # если сообщений нет, офсет устанавливается на                                                   # три месяца от текущей даты
    return oldest


async def parse(channel_name:str, client, url, key_words, bad_words):
    err = []  
    channel_id = await get_channel_id(client, url)  
    oldest = await find_last_parsed_date(channel_name, int(channel_id))
    tg_db = telegram_db(channel_name)
    if oldest is None: 
        return []
    oldest += relativedelta(seconds=1) 
    async for message in client.iter_messages(url, reverse=True, offset_date=oldest):
        await asyncio.sleep(0.5)
        try:
            if message.message:
                if (await get_text_from_filters(message, key_words, bad_words)):
                    await tg_db.create_new_telegram_channel_parsing(channel_id, message.date, clearify_text(message), message.id)
                else:
                    await tg_db.update_date_telegram_channel(channel_id, message.date)
            if message.media:
                post_exist = await tg_db.check_post_exist_in_telegram_channel(channel_id, datetime.datetime.strptime(message.date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
                if(post_exist):
                    url_path = await get_image(client, message, channel_id)
                    #print(url_path)
                    result = await tg_db.add_image_to_telegram_channel(channel_id, url_path, datetime.datetime.strptime(message.date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
                    if (result):
                        data = await get_image(client, message)
                        await add_file(url_path.split('/')[1], channel_id, data)
                else:
                    await tg_db.update_date_telegram_channel(channel_id, message.date)
        except Exception as passing: 
            print(f"Error {passing }")
            err.append(passing)
            continue
        if (os.path.isdir(f"{main_folder}/{channel_id}")): 
            shutil.rmtree(f"{main_folder}/{channel_id}")
    return err