import datetime
from base_connection_db import get_url_connection


    
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

