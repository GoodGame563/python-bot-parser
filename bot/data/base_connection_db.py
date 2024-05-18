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
