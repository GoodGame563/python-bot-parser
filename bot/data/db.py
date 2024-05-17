import pymongo
import os
import logging
import datetime
#ports = int(os.environ['ports'].split(':')[0])


def check_exist_database_if_create():
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
    info = client.info
    telegram_channels_collection = info.telegram_channels
    if telegram_channels_collection.count_documents({}) == 0:
        telegram_channels_collection.insert_many([
            {
                "id": 1107107975,
                "link_channel": 'https://t.me/brechalov',
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            },
            {
                "id": 1696477325,
                "link_channel": 'https://t.me/yaroslav_semenov',
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            },
            {
                "id": 2032566955,
                "link_channel": 'https://t.me/kommersant18',
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            },
            {
                "id": 1038973822,
                "link_channel": 'https://t.me/susaninudm',
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            },
            {
                "id": 1099350027,
                "link_channel": 'https://t.me/rusbrief',
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            }
        ])
    else:
      print("Alredy exsist telegram channels")
    key_words_collection = info.key_words
    if key_words_collection.count_documents({}) == 0:
        key_words_collection.insert_many([
          {"word":"экономик"},
          {"word":"бизнес"},
          {"word":"инвестиц"},
          {"word":"инвестиции"},
          {"word":"бюджет"},
          {"word":"a"}
        ])
    else:
      print("Alredy exsist key words")
    client.close()

def get_telegramm_channels():
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
    check_exist_database_if_create()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels = {}
    for channel in telegram_channels_collection.find():
      telegram_channels[channel['id']] = (channel['link_channel'], channel['last_updated'])
    client.close()
    return telegram_channels

def get_documents_from_channels_before_date(id: str, date):
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
    info = client.info
    telegram_channels_collection = info.get_collection(id)
    if type(date) == datetime.datetime:
        return telegram_channels_collection.find({"date":{"$gte": date}}).sort("_id")
    

def add_telegram_channel(url, id):
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels_collection.insert_one({
        "id": id,
        "link_channel": url,
        "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
    })
    client.close()

def delete_telegram_channel(id):
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels_collection.delete_one({"id": id})
    client.close()


def get_key_words():
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
    info = client.info
    key_words_collection = info.key_words
    key_words = {}
    for word in key_words_collection.find():
      key_words[word['_id']] = word['word']
    client.close()
    return key_words

def create_new_channel_parsing(id: str, date: datetime, text:str, id_collection:int):
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
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
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels_collection.update_one({"id": int(id)}, {"$set": {"last_updated": date}})
    client.close()


def check_post_exist(id:str, date:datetime):
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
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
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
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
    client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")
    info = client.info
    telegram_channels_collection = info.telegram_channels
    #print(id)
    result = telegram_channels_collection.find_one({"id": id})
    client.close()
    if result == None:
       print("none")
    else:   
        return result["last_updated"]

#print(check_post_exist(2054430930,  datetime.datetime.strptime("2024-05-10 19:26:48", '%Y-%m-%d %H:%M:%S')))
#print(return_data_last_changed_collection(2054430930))

#get_telegramm_channels()
#add_telegram_channel("https://t.me/piratecat24", 2054430930)
#url1 = ["mem.jpg", "dasdasd.jpg"]
#create_new_channel_parsing('1099350027', datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z"), "fdsfdsfsdfsdfsdfsfdsfsdfdsf", 3)
#add_image('1099350027',"fgdgfd",3, datetime.datetime.strptime("1970-02-01 00:00:00", "%Y-%m-%d %H:%M:%S"))