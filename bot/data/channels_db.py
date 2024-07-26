import os
import sys
from data.base_connection_db import get_url_connection
from datetime import datetime
from logs.loging import log_db

sys.path.append(os.path.join(os.getcwd(), '..'))
chat_send = os.environ.get('CHAT_ID')

async def check_channels_exist():
    try: 
        client  = get_url_connection()
        info = client.info
        channels_collection = info.channels
        if await  channels_collection.estimated_document_count() > 0:
            print ("Channels exist in database")
        else:
            for channel in chat_send.split(','):
                await channels_collection.insert_one({'id':channel.replace(' ', '')})
            print ("Channels not exist in database")
    except Exception:
        print("error")

async def return_channels_with_name():
    try: 
        client  = get_url_connection()
        info = client.info
        channels_collection = info.channels
        result = []
        async for channel in channels_collection.find():
            if channel.get("id") is not None:
                result.append([channel['id'], channel['name']])
        return result
    except Exception:
        print("error")

async def return_channels():
    try: 
        client  = get_url_connection()
        info = client.info
        channels_collection = info.channels
        result = []
        async for channel in channels_collection.find():
            if channel.get("id") is not None:
                result.append(channel['id'])
        return result
    except Exception:
        print("error")

async def add_channel(id:str, name:str):
    try:
        client  = get_url_connection()
        info = client.info
        channels = info.channels
        await channels.insert_one({
            "id": str(id), 
            "name": name
        })
        chat = client[str(id)]
        chat_settings = chat.settings
        if await chat_settings.estimated_document_count() == 0:
            await chat_settings.insert_one({
                "posting_image": True,
                "link_to_source": True,
                "work_on_time": False,
                "parser": False,
                "send_post": False,
                "neural_enabled": False,
                "work_on_time": False,
                "start_time": datetime.strptime("09:00:00", "%H:%M:%S"),
                "end_time": datetime.strptime("21:00:00", "%H:%M:%S")
            })
    except Exception:
        print("error")

async def delete_channel(id):
    try:
        client  = get_url_connection()
        info = client.info
        channels = info.channels
        await channels.delete_one({
            "id": str(id)
        })
        await client.drop_database(str(id))
    except Exception:
        print("error")
    
async def return_in_channel_channels(id):
    try:
        client  = get_url_connection()
        channel = client[id]
        channels_collection = channel.telegram_channels
        result = []
        async for channel in channels_collection.find():
            result.append([ channel['id'], channel['link_channel']])
        return result
    except Exception:
        print("error")

async def return_rss_in_channel(id):
    client  = get_url_connection()
    channel = client[id]
    channels_collection = channel.url_sites
    result = []
    async for channel in channels_collection.find():
        result.append([channel["_id"], channel["url"]])
    return result
