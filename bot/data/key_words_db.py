from data.base_connection_db import get_url_connection

from logs.loging import log_db

async def get_key_words():
    log_db().send_info("Starting get_key_words() function.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None
    
    log_db().send_debug("URL connection established.")
    
    try:
        client = connection
        info = client.info
        key_words_collection = info.key_words
        key_words = {}
        
        log_db().send_debug("Fetching key words from collection.")
        async for word in key_words_collection.find():
            key_words[word['_id']] = word['word']
        
        log_db().send_info("Key words successfully fetched.")
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
    return key_words

async def add_key_words(words: list):
    log_db().send_info("Starting add_key_words() function.")
    try:
        client = get_url_connection()
        info = client.info
        key_words_collection = info.key_words     
        words_collection = list()
        for word in words:
            if await key_words_collection.count_documents({"word": str(word)}) == 0:
                words_collection.append({
                    "word": str(word)
                })
        if len(words_collection) != 0:
            await key_words_collection.insert_many(words_collection)
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None

async def reduct_key_word(old_word:str, new_word:str):
    log_db().send_info("Starting reduct_key_word() function.")
    try:
        client  = get_url_connection()
        info = client.info
        key_words_collection = info.key_words     
        if await key_words_collection.count_documents({"word": str(old_word)}) == 1:
            await key_words_collection.update_one({"word": str(old_word)},{'$set': {"word": str(new_word)}})
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None

async def delete_key_words(words:list):
    log_db().send_info("Starting delete_key_words() function.")
    try:
        client  = get_url_connection()
        info = client.info
        key_words_collection = info.key_words     
        for word in words:
            if await key_words_collection.count_documents({"word": str(word)}) != 0:
                await key_words_collection.delete_one({"word": str(word)})   
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None