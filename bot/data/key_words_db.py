from data.base_connection_db import get_url_connection

from logs.loging import log_db
from bson import ObjectId

class words_db:
    def __init__(self, table: str, id_channel: int):
        self.table = table
        self.id = id_channel
    async def get_key_words(self):
        log_db().send_info("Starting get_key_words() function.")

        connection = get_url_connection()
        key_words = []
        try:
            client = connection
            info = client[self.table]
            key_words_collection = await info.telegram_channels.find_one({"id": int(self.id)})
            key_words_collection = key_words_collection['key_words']
            for word in key_words_collection:
                key_words.append(word)
            
            log_db().send_info("Key words successfully fetched.")
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None
        return key_words
    
    async def get_del_words(self):
        log_db().send_info("Starting get_del_words() function.")

        connection = get_url_connection()
        key_words = []
        try:
            client = connection
            info = client[self.table]
            key_words_collection = await info.telegram_channels.find_one({"id": int(self.id)})
            key_words_collection = key_words_collection['bad_words']
            for word in key_words_collection:
                key_words.append(word)
            
            log_db().send_info("Key words successfully fetched.")
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None
        return key_words

    async def add_key_words(self, words: list):
        log_db().send_info("Starting add_key_words() function.")
        try:
            client = get_url_connection()
            info = client[self.table]
            key_words_collection = await info.telegram_channels.find_one({"id": int(self.id)})
            key_words_collection = key_words_collection['key_words']

            await info.telegram_channels.find_one_and_update({"id": int(self.id)}, {"$set": {"key_words": key_words_collection + words}})  
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None
        
    async def add_bad_words(self, words: list):
        log_db().send_info("Starting add_key_words() function.")
        try:
            client = get_url_connection()
            info = client[self.table]
            key_words_collection = await info.telegram_channels.find_one({"id": int(self.id)})
            key_words_collection = key_words_collection['bad_words']

            await info.telegram_channels.find_one_and_update({"id": int(self.id)}, {"$set": {"bad_words": key_words_collection + words}})  
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None

    async def delete_key_words(self, words:list):
        log_db().send_info("Starting delete_key_words() function.")
        try:
            client  = get_url_connection()
            info = client[self.table]
            key_words_collection = await info.telegram_channels.find_one({"id": int(self.id)})
            key_words_collection = key_words_collection['key_words']
            for word in words:
                while key_words_collection.count(word) > 0:
                    key_words_collection.remove(word)
            await info.telegram_channels.find_one_and_update({"id": int(self.id)}, {"$set": {"key_words": key_words_collection}})  
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None
        
    async def delete_bad_words(self, words:list):
        log_db().send_info("Starting delete_key_words() function.")
        try:
            client  = get_url_connection()
            info = client[self.table]
            key_words_collection = await info.telegram_channels.find_one({"id": int(self.id)})
            key_words_collection = key_words_collection['bad_words']
            for word in words:
                while key_words_collection.count(word) > 0:
                    key_words_collection.remove(word)
            await info.telegram_channels.find_one_and_update({"id": int(self.id)}, {"$set": {"bad_words": key_words_collection}})  
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None


class sites_words_db:
    def __init__(self, table: str, id_channel: str):
        self.table = table
        self.id = id_channel
    async def get_key_words(self):
        log_db().send_info("Starting get_key_words() function.")

        connection = get_url_connection()
        key_words = []
        try:
            client = connection
            info = client[self.table]
            key_words_collection = await info.url_sites.find_one({"_id": ObjectId(self.id)})
            key_words_collection = key_words_collection['key_words']
            for word in key_words_collection:
                key_words.append(word)
            
            log_db().send_info("Key words successfully fetched.")
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None
        return key_words
    
    async def get_del_words(self):
        log_db().send_info("Starting get_del_words() function.")

        connection = get_url_connection()
        key_words = []
        try:
            client = connection
            info = client[self.table]
            key_words_collection = await info.url_sites.find_one({"_id": ObjectId(self.id)})
            key_words_collection = key_words_collection['bad_words']
            for word in key_words_collection:
                key_words.append(word)
            
            log_db().send_info("Key words successfully fetched.")
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None
        return key_words

    async def add_key_words(self, words: list):
        log_db().send_info("Starting add_key_words() function.")
        try:
            client = get_url_connection()
            info = client[self.table]
            key_words_collection = await info.url_sites.find_one({"_id": ObjectId(self.id)})
            key_words_collection = key_words_collection['key_words']

            await info.url_sites.find_one_and_update({"_id": ObjectId(self.id)}, {"$set": {"key_words": key_words_collection + words}})  
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None
        
    async def add_bad_words(self, words: list):
        log_db().send_info("Starting add_key_words() function.")
        try:
            client = get_url_connection()
            info = client[self.table]
            key_words_collection = await info.url_sites.find_one({"_id": ObjectId(self.id)})
            key_words_collection = key_words_collection['bad_words']

            await info.url_sites.find_one_and_update({"_id": ObjectId(self.id)}, {"$set": {"bad_words": key_words_collection + words}})  
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None

    async def delete_key_words(self, words:list):
        log_db().send_info("Starting delete_key_words() function.")
        try:
            client  = get_url_connection()
            info = client[self.table]
            key_words_collection = await info.url_sites.find_one({"_id": ObjectId(self.id)})
            key_words_collection = key_words_collection['key_words']
            for word in words:
                while key_words_collection.count(word) > 0:
                    key_words_collection.remove(word)
            await info.url_sites.find_one_and_update({"_id": ObjectId(self.id)}, {"$set": {"key_words": key_words_collection}})  
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None
        
    async def delete_bad_words(self, words:list):
        log_db().send_info("Starting delete_key_words() function.")
        try:
            client  = get_url_connection()
            info = client[self.table]
            key_words_collection = await info.url_sites.find_one({"_id": ObjectId(self.id)})
            key_words_collection = key_words_collection['bad_words']
            for word in words:
                while key_words_collection.count(word) > 0:
                    key_words_collection.remove(word)
            await info.url_sites.find_one_and_update({"_id": ObjectId(self.id)}, {"$set": {"bad_words": key_words_collection}})  
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None