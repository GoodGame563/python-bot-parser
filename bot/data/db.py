import pymongo
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
url_connection = os.environ.get('DATA_DB_URL')
root_user = os.environ.get('DATA_DB_ROOT_USER')
root_password = os.environ.get('DATA_DB_ROOT_PASS')
port = os.environ.get('DATA_DB_PORT_DESKTOP')

def get_url_connection():
    if(url_connection is None):
        return None
    if(root_user is None):
        return None
    if(root_password is None):
        return None
    if(port is None):
        return None
    return pymongo.MongoClient(f"mongodb://{root_user}:{root_password}@{url_connection}:{port}/")
    
def check_exist_database_if_create():
    telegram_channels_collection = list()
    if(os.environ.get('DEFAULT_VALUES_TELEGRAMM_CHANNELS_Id') is None):
        return None
    if(os.environ.get('DEFAULT_VALUES_TELEGRAMM_CHANNELS_Path') is None):
        return None
    id_channels_collection = os.environ.get('DEFAULT_VALUES_TELEGRAMM_CHANNELS_Id').replace(" ","").split(",")
    path_channels_collection = os.environ.get('DEFAULT_VALUES_TELEGRAMM_CHANNELS_Path').replace(" ","").split(",")
    if(len(id_channels_collection) != len(path_channels_collection)):
        return None
    for i in range(len(id_channels_collection)):
        telegram_channels_collection.append({
            "id": int(id_channels_collection[i]),
            "link_channel": path_channels_collection[i],
            "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
        })
    
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    
    info = client.info
    telegram_channels_table = info.telegram_channels

    if telegram_channels_table.count_documents({}) != 0:
        print("Alredy exsist telegram channels")
        return True
    words = os.environ.get('DEFAULT_VALUES_WORDS')
    if(words is not None):
        words_collection = list()
        for word in words.replace(" ","").split(","):
            words_collection.append({
                "word": word
            })

        key_words_collection = info.key_words
        if key_words_collection.count_documents({}) == 0:
            key_words_collection.insert_many(words_collection)
        else:
            print("Alredy exsist key words")
    if telegram_channels_table.count_documents({}) == 0: telegram_channels_table.insert_many(telegram_channels_collection)
    client.close()

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

def get_documents_from_channels_before_date(id: str, date: datetime.datetime):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.get_collection(id)
    if type(date) == datetime.datetime:
        return telegram_channels_collection.find({"date":{"$gte": date}}).sort("_id")
    
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
            "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
        })
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

def delete_telegram_channel(id: int):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels_collection.delete_one({"id": id})
    client.close()

def get_key_words():
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    key_words_collection = info.key_words
    key_words = {}
    for word in key_words_collection.find():
      key_words[word['_id']] = word['word']
    client.close()
    return key_words

def create_new_channel_parsing(id: str, date: datetime, text:str, id_collection:int):
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

def update_data(id: str, date: datetime):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels_collection.update_one({"id": int(id)}, {"$set": {"last_updated": date}})
    client.close()

def check_post_exist(id:str, date:datetime):
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

def add_image(id:str, url, date:datetime):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channel_collection = info.get_collection(id)
    result = telegram_channel_collection.find_one({"date": date})
    if result is not None:
        if result["date"] == date:
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
            print("даты не совпадают")
            client.close()
            return False
    else:
        return False

def return_data_last_changed_collection(id: int):
    if(get_url_connection() is None):
        return None
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    #print(id)
    result = telegram_channels_collection.find_one({"id": id})
    client.close()
    if result == None:
       print("none")
    else:   
        return result["last_updated"]

#print(check_telegram_channel(2032566952))