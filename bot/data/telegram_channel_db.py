from data.base_connection_db import get_url_connection
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from logs.loging import log_db

#work with collection
def add_telegram_channel(url: str, id: int):

    log_db().send_info("Starting add_telegram_channel() function.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        telegram_channels_collection = info.telegram_channels

        if get_telegram_channel_by_id(id) is None:
            log_db().send_info(f"Channel with ID {id} does not exist. Inserting new channel.")
            telegram_channels_collection.insert_one({
                "id": int(id),
                "link_channel": url,
                "last_updated": datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            })
            log_db().send_info(f"Channel with ID {id} added successfully.")
            return True
        else:
            log_db().send_warning(f"Channel with ID {id} already exists.")
            return False
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")

def delete_telegram_channel(id: int):
    log_db().send_info(f"Starting delete_telegram_channel() function for channel ID {id}.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    client = connection
    info = client.info
    telegram_channels_collection = info.telegram_channels

    try:
        log_db().send_debug(f"Attempting to delete channel with ID {id}.")
        result = telegram_channels_collection.delete_one({"id": id})
        
        if result.deleted_count == 0:
            log_db().send_info(f"No channel found with ID {id} to delete.")
            return False
        else:
            log_db().send_info(f"Channel with ID {id} deleted successfully.")
            return True
    except Exception as e:
        log_db().send_critical(f"An error occurred while deleting channel with ID {id}: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")

def get_telegram_channel_by_id(id: int):
    log_db().send_info(f"Starting get_telegram_channel_by_id() function for channel ID {id}.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        telegram_channels_collection = info.telegram_channels

        log_db().send_debug(f"Checking if channel with ID {id} exists.")
        channel = telegram_channels_collection.find_one({"id": id})
        
        if channel is None:
            log_db().send_info(f"Telegram channel with ID {id} not found.")
            return None
        else:
            log_db().send_info(f"Telegram channel with ID {id} found.")
            return channel
    except Exception as e:
        log_db().send_critical(f"An error occurred while checking channel with ID {id}: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")

def get_telegram_channels_by_url(url: str):
    log_db().send_info(f"Starting get_telegramm_channels_by_url() function for channel URL {url}.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        telegram_channels_collection = info.telegram_channels

        log_db().send_debug(f"Checking if channel with URL {url} exists.")
        channel = telegram_channels_collection.find_one({"link_channel": url})
        
        if channel is None:
            log_db().send_info(f"Telegram channel with URL {url} not found.")
            return None
        else:
            log_db().send_info(f"Telegram channel with URL {url} found.")
            return channel
    except Exception as e:
        log_db().send_critical(f"An error occurred while checking channel with URL {url}: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")

def update_date_telegram_channel(id: int, date: datetime):
    log_db().send_info(f"Starting update_date_telegram_channel() function for channel ID {id}.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        telegram_channels_collection = info.telegram_channels

        log_db().send_debug(f"Updating last_updated for channel with ID {id}.")
        result = telegram_channels_collection.update_one(
            {"id": int(id)},
            {"$set": {"last_updated": date}}
        )
        
        if result.modified_count == 0:
            log_db().send_info(f"Telegram channel with ID {id} not found.")
            return False
        else:
            log_db().send_info(f"Telegram channel with ID {id} updated successfully.")
            return True
    except Exception as e:
        log_db().send_critical(f"An error occurred while updating channel with ID {id}: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")

def get_telegramm_channels():
    log_db().send_info("Starting get_telegramm_channels() function.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        telegram_channels_collection = info.telegram_channels

        log_db().send_debug("Fetching telegram channels from the database.")
        telegram_channels = {}
        for channel in telegram_channels_collection.find():
            if channel.get("id") is not None:
                telegram_channels[channel['id']] = (channel['link_channel'], channel['last_updated'])

        if len(telegram_channels) == 0:
            log_db().send_info("No telegram channels found.")
        else:
            log_db().send_info(f"Found {len(telegram_channels)} telegram channels.")
            
        return telegram_channels
    except Exception as e:
        log_db().send_critical(f"An error occurred while fetching telegram channels: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")


#work with documents 
def check_post_exist_in_telegram_channel(id: str, date: datetime):
    log_db().send_info(f"Starting check_post_exist_in_telegram_channel() function for channel ID {id} and date {date}.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        collections = info.list_collection_names()

        if str(id) in collections:
            log_db().send_info(f"Channel collection for ID {id} found.")
            telegram_channel_collection = info.get_collection(id)
            result = telegram_channel_collection.find_one({"date": date})
            
            if result is not None and result["date"] == date:
                log_db().send_info(f"Post with date {date} found in channel ID {id}.")
                return True
            else:
                log_db().send_info(f"No post with date {date} found in channel ID {id}.")
                return False
        else:
            log_db().send_info(f"Channel collection for ID {id} does not exist.")
            return False
    except Exception as e:
        log_db().send_critical(f"An error occurred while checking post in channel ID {id}: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")

def add_image_to_telegram_channel(id: str, url: str, date: datetime):
    log_db().send_info(f"Starting add_image_to_telegram_channel() function for channel ID {id}, URL {url}, and date {date}.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        telegram_channel_collection = info.get_collection(id)

        log_db().send_debug(f"Checking if post with date {date} exists in channel ID {id}.")
        result = telegram_channel_collection.find_one({"date": date})
        
        if result is not None:
            log_db().send_info(f"Post with date {date} found in channel ID {id}.")
            if result.get('count_img') is None:
                telegram_channel_collection.update_one({"date": date}, {"$set": {"count_img": 1}})
                telegram_channel_collection.update_one({"date": date}, {"$set": {"url": [url]}})
                log_db().send_info(f"Image URL {url} added to post with date {date} and initialized count_img.")
            else:
                telegram_channel_collection.update_one({"date": date}, {"$set": {"count_img": result.get('count_img') + 1}})
                urls = result.get('url', [])
                urls.append(url)
                telegram_channel_collection.update_one({"date": date}, {"$set": {"url": urls}})
                log_db().send_info(f"Image URL {url} added to post with date {date}. count_img updated.")

            return True
        else:
            log_db().send_info(f"Post with date {date} not found in channel ID {id}.")
            return False
    except Exception as e:
        log_db().send_critical(f"An error occurred while adding image to channel ID {id}: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")
    
def create_new_telegram_channel_parsing(id: str, date: datetime, text: str, id_collection: int):
    log_db().send_info(f"Starting create_new_telegram_channel_parsing() function for channel ID {id}, date {date}, and text {text[:30]}...")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        telegram_channels_collection = info.get_collection(id)

        log_db().send_info(f"Inserting new post with ID {id_collection} into channel ID {id}.")
        telegram_channels_collection.insert_one({
            "_id": int(id_collection),
            "date": date,
            "text": text
        })

        telegram_channels_collection = info.telegram_channels
        log_db().send_info(f"Updating last_updated for channel ID {id} to {date}.")
        telegram_channels_collection.update_one({"id": int(id)}, {"$set": {"last_updated": date}})

        log_db().send_info(f"New post created and last_updated updated successfully for channel ID {id}.")
    except Exception as e:
        log_db().send_critical(f"An error occurred while creating new post for channel ID {id}: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")

def return_data_last_changed_telegram_channel(id: int):
    log_db().send_info(f"Starting return_data_last_changed_telegram_channel() function for channel ID {id}.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        telegram_channels_collection = info.telegram_channels

        log_db().send_debug(f"Fetching last_updated for channel ID {id}.")
        result = telegram_channels_collection.find_one({"id": id})

        if result is None:
            log_db().send_info(f"Telegram channel with ID {id} not found.")
            return None
        elif result.get("last_updated") is None:
            log_db().send_info(f"Telegram channel with ID {id} does not have a last_updated field.")
            return None
        else:
            log_db().send_info(f"Telegram channel with ID {id} found. Returning last_updated.")
            return result.get("last_updated")
    except Exception as e:
        log_db().send_critical(f"An error occurred while fetching last_updated for channel ID {id}: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")
    
def get_documents_from_telegram_channels_before_date(id: str, date: datetime):
    log_db().send_info(f"Starting get_documents_from_telegram_channels_before_date() function for channel ID {id} and date {date}.")

    connection = get_url_connection()
    if connection is None:
        log_db().send_error("Failed to get URL connection.")
        return None

    log_db().send_debug("URL connection established.")

    try:
        client = connection
        info = client.info
        telegram_channels_collection = info.get_collection(id)

        log_db().send_info(f"Fetching documents from channel ID {id} before date {date}.")
        if isinstance(date, datetime):
            documents = telegram_channels_collection.find({"date": {"$gte": date}}).sort("_id")
            log_db().send_info(f"Documents fetched successfully from channel ID {id} before date {date}.")
            return documents
        else:
            log_db().send_error("Provided date is not of type datetime.")
            return None
    except Exception as e:
        log_db().send_critical(f"An error occurred while fetching documents from channel ID {id}: {str(e)}")
        return None
    finally:
        client.close()
        log_db().send_debug("URL connection closed.")