import datetime
import sys
import os
from data.base_connection_db import get_url_connection
sys.path.append(os.path.join(os.getcwd(), '..'))

from logs.loging import log_db

def get_all_settings():
    try:
        connection = get_url_connection()
        if connection is None:
            log_db().send_error("Failed to get URL connection.")
            return None
        
        log_db().send_debug("URL connection established.")

        client = connection
        info = client.info
        settings = info.settings  
        if settings.estimated_document_count == 0:
            return None
        return settings.find_one()
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_info("URL connection closed.")

def switch_mode_parser(mode: bool):
    try:
        connection = get_url_connection()
        if connection is None:
            log_db().send_error("Failed to get URL connection.")
            return None
        
        log_db().send_debug("URL connection established.")
        client = connection
        info = client.info
        settings = info.settings  
        settings.update_one({'_id':1},{'$set':{'parser':bool(mode)}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_info("URL connection closed.")

def switch_mode_send_post(mode: bool):
    try:
        connection = get_url_connection()
        if connection is None:
            log_db().send_error("Failed to get URL connection.")
            return None
        
        log_db().send_debug("URL connection established.")
        client = connection
        info = client.info
        settings = info.settings  
        settings.update_one({'_id':1},{'$set':{'send_post':bool(mode)}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_info("URL connection closed.")

def turn_on_work_on_time(start_time: datetime.datetime.time, end_time: datetime.datetime.time):
    try:
        connection = get_url_connection()
        if connection is None:
            log_db().send_error("Failed to get URL connection.")
            return None
        
        log_db().send_debug("URL connection established.")
        client = connection
        info = client.info
        settings = info.settings  
        settings.update_one({'_id':1},{'$set': {'work_on_time':True}})
        settings.update_one({'_id':1},{'$set': {'start_time':start_time}})
        settings.update_one({'_id':1},{'$set': {'end_time':end_time}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_info("URL connection closed.")

def turn_off_work_on_time():
    try:
        connection = get_url_connection()
        if connection is None:
            log_db().send_error("Failed to get URL connection.")
            return None
        
        log_db().send_debug("URL connection established.")
        client = connection
        info = client.info
        settings = info.settings  
        settings.update_one({'_id':1},{'$set': {'work_on_time':False}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_info("URL connection closed.")

