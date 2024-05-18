from base_connection_db import get_url_connection
from datetime import datetime

def add_telegram_channel(url: str, id: int):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    if check_telegram_channel(id) is None:
        telegram_channels_collection.insert_one({
            "id": int(id),
            "link_channel": url,
            "last_updated": datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
        })
    client.close()

def delete_telegram_channel(id: int):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels_collection.delete_one({"id": id})
    client.close()


def check_telegram_channel(id: int):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    channel = telegram_channels_collection.find_one({"id": id})
    if channel is None:
        return None
    client.close()
    return channel

def update_data_telegram_channel(id: str, date: datetime):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels_collection.update_one({"id": int(id)}, {"$set": {"last_updated": date}})
    client.close()

def check_post_exist_in_telegram_channel(id:str, date:datetime):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    collections = info.list_collection_names()
    if str(id) in collections:
        telegram_channel_collection = info.get_collection(id)
        result = telegram_channel_collection.find_one({"date": date})
        if result is not None:
            if result["date"] == date:
                return True
            return False
    return False

def add_image_to_telegram_channel(id:str, url, date:datetime):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channel_collection = info.get_collection(id)
    result = telegram_channel_collection.find_one({"date": date})
    if result is not None:
        if(result.get('count_img') == None):
            telegram_channel_collection.update_one({"date": date}, {"$set": {"count_img": 1}})
            telegram_channel_collection.update_one({"date": date}, {"$set": {"url": [url]}})
        else:
            telegram_channel_collection.update_one({"date": date}, {"$set": {"count_img": result.get('count_img')+1}})
            count = result.get('url')
            count.append(url)
            telegram_channel_collection.update_one({"date": date}, {"$set": {"url": count}})
        client.close()
        return True
    else:
        return False
    
def create_new_telegram_channel_parsing(id: str, date: datetime, text:str, id_collection:int):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.get_collection(id)
    telegram_channels_collection.insert_one({
        "_id": int(id_collection),
        "date": date,
        "text": str(text)
    })
    telegram_channels_collection = info.telegram_channels
    telegram_channels_collection.update_one({"id": int(id)}, {"$set": {"last_updated": date}})
    client.close()

def return_data_last_changed_telegram_channel(id: int):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    result = telegram_channels_collection.find_one({"id": id})
    client.close()
    if result == None:
       print("none")
    else:   
        return result["last_updated"]

def get_telegramm_channels():
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels = {}
    for channel in telegram_channels_collection.find():
        if channel.get("id") is not None:
            telegram_channels[channel['id']] = (channel['link_channel'], channel['last_updated'])
    client.close()
    return telegram_channels

def get_documents_from_telegram_channels_before_date(id: str, date: datetime.datetime):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.get_collection(id)
    if type(date) == datetime.datetime:
        return telegram_channels_collection.find({"date":{"$gte": date}}).sort("_id")