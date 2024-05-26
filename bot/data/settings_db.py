import datetime
from data.base_connection_db import get_url_connection

from logs.loging import log_db

async def get_all_settings():
    try:
        client = get_url_connection()
        info = client.info
        settings = info.settings  
        return await settings.find_one()
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None

async def switch_mode_parser(mode: bool):
    try:
        client  = get_url_connection()
        info = client.info
        settings = info.settings  
        await settings.update_one({'_id':1},{'$set':{'parser':bool(mode)}})
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None

async def switch_mode_send_post(mode: bool):
    try:
        client  = get_url_connection()
        info = client.info
        settings = info.settings  
        await settings.update_one({'_id':1},{'$set':{'send_post':bool(mode)}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None

async def turn_on_work_on_time(start_time: datetime.datetime.time, end_time: datetime.datetime.time):
    try:
        client  = get_url_connection()
        info = client.info
        settings = info.settings  
        await settings.update_one({'_id':1},{'$set': {'work_on_time':True}})
        await settings.update_one({'_id':1},{'$set': {'start_time':start_time}})
        await settings.update_one({'_id':1},{'$set': {'end_time':end_time}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None

async def turn_off_work_on_time():
    try:
        client  = get_url_connection()
        info = client.info
        settings = info.settings  
        await settings.update_one({'_id':1},{'$set': {'work_on_time':False}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None

async def switch_mode_send_image(mode: bool):
    try:
        client  = get_url_connection()
        info = client.info
        settings = info.settings  
        await settings.update_one({'_id':1},{'$set':{'posting_image':bool(mode)}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None

async def switch_mode_send_links(mode: bool):
    try:
        client  = get_url_connection()
        info = client.info
        settings = info.settings  
        await settings.update_one({'_id':1},{'$set':{'link_to_source':bool(mode)}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None

async def switch_mode_neural_network(mode: bool):
    try:
        client  = get_url_connection()
        info = client.info
        settings = info.settings  
        await settings.update_one({'_id':1},{'$set':{'neural_enabled':bool(mode)}})

    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None