import pymongo
import os
import datetime
import sys
from dotenv import load_dotenv
sys.path.append(os.path.join(os.getcwd(), '..'))

from logs.loging import log_db


load_dotenv()

url_connection = os.environ.get('DATA_DB_URL')
root_user = os.environ.get('DATA_DB_ROOT_USER')
root_password = os.environ.get('DATA_DB_ROOT_PASS')
port = os.environ.get('DATA_DB_PORT_DESKTOP')

def get_url_connection():
    if(url_connection is None):
        log_db().send_critical('Could not connect to database, Error: url_connection is none')
        return None
    if(root_user is None):
        log_db().send_critical('Could not connect to database, Error: root_user is none')
        return None
    if(root_password is None):
        log_db().send_critical('Could not connect to database, Error: root_password is none')
        return None
    if(port is None):
        log_db().send_critical('Could not connect to database, Error: port is none')
        return None
    return pymongo.MongoClient(f"mongodb://{root_user}:{root_password}@{url_connection}:{port}/")

def check_exist_database_if_create():
    log_db().send_info("Starting check_exist_database_if_create() function.")

    telegram_channels_collection = list()
    
    default_ids = os.environ.get('DEFAULT_VALUES_TELEGRAMM_CHANNELS_Id')
    default_paths = os.environ.get('DEFAULT_VALUES_TELEGRAMM_CHANNELS_Path')
    
    if default_ids is None:
        log_db().send_error("Environment variable 'DEFAULT_VALUES_TELEGRAMM_CHANNELS_Id' is not set.")
        return None
    if default_paths is None:
        log_db().send_error("Environment variable 'DEFAULT_VALUES_TELEGRAMM_CHANNELS_Path' is not set.")
        return None

    id_channels_collection = default_ids.replace(" ", "").split(",")
    path_channels_collection = default_paths.replace(" ", "").split(",")
    
    if len(id_channels_collection) != len(path_channels_collection):
        log_db().send_warning("Mismatch between the number of IDs and paths.")
        return None

    for i in range(len(id_channels_collection)):
        telegram_channels_collection.append({
            "id": int(id_channels_collection[i]),
            "link_channel": path_channels_collection[i],
            "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z"),
            "last_send": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
        })
    
    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    client = connection
    info = client.info
    telegram_channels_table = info.telegram_channels

    try:
        if telegram_channels_table.count_documents({}) != 0:
            log_db().send_info("Telegram channels already exist in the database.")
            return True

        words = os.environ.get('DEFAULT_VALUES_WORDS')
        if words is not None:
            words_collection = list()
            for word in words.replace(" ", "").split(","):
                words_collection.append({
                    "word": word
                })

            key_words_collection = info.key_words
            if key_words_collection.count_documents({}) == 0:
                log_db().send_debug("Inserting default key words into the database.")
                key_words_collection.insert_many(words_collection)
            else:
                log_db().send_info("Key words already exist in the database.")

        if telegram_channels_table.count_documents({}) == 0:
            log_db().send_debug("Inserting default telegram channels into the database.")
            telegram_channels_table.insert_many(telegram_channels_collection)

        log_db().send_info("Database check and setup completed successfully.")
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_info("URL connection closed.")