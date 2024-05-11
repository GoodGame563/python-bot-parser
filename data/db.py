import pymongo
import os
import logging
import datetime
#ports = int(os.environ['ports'].split(':')[0])
client = pymongo.MongoClient(f"mongodb://root:root@localhost:8000/")

def check_exist_database_if_create():
    info = client.info
    telegram_channels_collection = info.telegram_channels
    if telegram_channels_collection.count_documents({}) == 0:
        telegram_channels_collection.insert_many([
            {
                "_id": 1107107975,
                "link_channel": 'https://t.me/brechalov',
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            },
            {
                "_id": 1696477325,
                "link_channel": 'https://t.me/yaroslav_semenov',
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            },
            {
                "_id": 2032566955,
                "link_channel": 'https://t.me/kommersant18',
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            },
            {
                "_id": 1038973822,
                "link_channel": 'https://t.me/susaninudm',
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            },
            {
                "_id": 1099350027,
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

def get_telegramm_channels():
    check_exist_database_if_create()
    info = client.info
    telegram_channels_collection = info.telegram_channels
    telegram_channels = {}
    for channel in telegram_channels_collection.find():
      telegram_channels[channel['_id']] = (channel['link_channel'], channel['last_updated'])
    return telegram_channels

def get_key_words():
    check_exist_database_if_create()
    info = client.info
    key_words_collection = info.key_words
    key_words = {}
    for word in key_words_collection.find():
      key_words[word['_id']] = word['word']
    return key_words

print(get_telegramm_channels())
print(get_key_words())