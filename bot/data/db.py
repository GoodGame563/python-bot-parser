import datetime
import sys
import os
from data.base_connection_db import get_url_connection
sys.path.append(os.path.join(os.getcwd(), '..'))

from logs.loging import log_db
    
def get_key_words():
    log_db().send_info("Starting get_key_words() function.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None
    
    log_db().send_info("URL connection established.")
    
    try:
        client = connection
        info = client.info
        key_words_collection = info.key_words
        key_words = {}
        
        log_db().send_debug("Fetching key words from collection.")
        for word in key_words_collection.find():
            key_words[word['_id']] = word['word']
        
        log_db().send_info("Key words successfully fetched.")
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_info("URL connection closed.")

    return key_words

