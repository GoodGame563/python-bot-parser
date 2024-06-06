from data.base_connection_db import get_url_connection
from datetime import datetime
from logs.loging import log_db
from bson import ObjectId

#work with collection

async def get_sites_by_url(url: str):
    log_db().send_info(f"Starting get_sites_by_url() function for channel URL {url}.")
    try:
        client  = get_url_connection()
        info = client.info
        url_sites_collection = info.url_sites

        log_db().send_debug(f"Checking if sites with URL {url} exists.")
        channel = await url_sites_collection.find_one({"url": url})
        
        if channel is None:
            log_db().send_info(f"Telegram sites with URL {url} not found.")
            return None
        else:
            log_db().send_info(f"Telegram sites with URL {url} found.")
            return channel
    except Exception as e:
        log_db().send_critical(f"An error occurred while checking channel with URL {url}: {str(e)}")
        return None

async def get_sites_by_id(id: ObjectId):
    log_db().send_info(f"Starting get_sites_by_id() function for channel ID {id}.")
    try:
        client = get_url_connection()
        info = client.info
        url_sites_collection = info.url_sites

        log_db().send_debug(f"Checking if channel with ID {id} exists.")
        channel = await url_sites_collection.find_one({"_id": id})
        
        if channel is None:
            log_db().send_info(f"Telegram channel with ID {id} not found.")
            return None
        else:
            log_db().send_info(f"Telegram channel with ID {id} found.")
            return channel
    except Exception as e:
        log_db().send_critical(f"An error occurred while checking channel with ID {id}: {str(e)}")
        return None

async def update_date_sites(url: str, date: datetime):
    log_db().send_info(f"Starting update_date_sites() function for channel url {url}.")
    client  = get_url_connection()
    info = client.info
    url_sites_collection = info.url_sites
    try:
        log_db().send_debug(f"Updating update_date_sites() for channel with url {url}.")
        await url_sites_collection.update_one(
            {"url": url},
            {"$set": {"last_updated": date}}
        )
    except Exception as e:
        log_db().send_critical(f"An error occurred while updating channel with ID {id}: {str(e)}")
        return None

async def get_sites():
    log_db().send_info("Starting get_sites() function.")
    client  = get_url_connection()
    info = client.info
    url_sites_collection = info.url_sites

    try:
        sites = {}
        async for channel in url_sites_collection.find():
            if channel.get("url") is not None:
                sites[str(channel['url']).replace("www.", "").split("/")[2].split(".")[0]] = (channel['url'], channel['last_updated'], channel['last_send'])

        if len(sites) == 0:
            log_db().send_info("No sites found.")
        else:
            log_db().send_info(f"Found {len(sites)} telegram channels.")    
        return sites
    except Exception as e:
        log_db().send_critical(f"An error occurred while fetching telegram channels: {str(e)}")
        return None

async def update_sites_last_send(url:str, date: datetime):
    log_db().send_info(f"Starting update_sites_last_send() function for sites url {url}.")
    client  = get_url_connection()
    info = client.info
    url_sites_collection = info.url_sites
    try:
        log_db().send_debug(f"Updating last_updated for sites with url {url}.")
        await url_sites_collection.update_one(
            {"url": url},
            {"$set": {"last_send": date}}
        )  
    except Exception as e:
        log_db().send_critical(f"An error occurred while updating channel with ID {id}: {str(e)}")
        return None

async def exists_new_update(id: ObjectId):
    log_db().send_info(f"Starting exists_new_update() function for channel ID {id}.")
    try:
        sites = await get_sites_by_id(id)
        if sites is not None:
            last_send = sites.get("last_send")
            last_update = sites.get("last_updated")
            if last_send is None:
                log_db().send_info(f"Telegram channel with ID {id} does not have last_send.")
                return False
            else:
                log_db().send_info(f"Telegram channel with ID {id} has last_send.")
                if last_send != last_update:
                    return True
                else:
                    return False     
    except Exception as e:
        log_db().send_critical(f"An error occurred while updating channel with ID {id}: {str(e)}")
        return None


#work with documents 
async def check_post_exist_in_telegram_channel(id: str, date: datetime):
    log_db().send_info(f"Starting check_post_exist_in_telegram_channel() function for channel ID {id} and date {date}.")

    client  = get_url_connection()
    info = client.info
    collections = await info.list_collection_names()

    try:
        if str(id) in collections:
            log_db().send_info(f"Channel collection for ID {id} found.")
            telegram_channel_collection = info.get_collection(id)
            result = await telegram_channel_collection.find_one({"date": date})
            
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
    
async def create_new_sites_parsing(id: str, date: datetime, text: str, id_collection: int):
    log_db().send_info(f"Starting create_new_telegram_channel_parsing() function for channel ID {id}, date {date}, and text {text[:30]}...")

    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.get_collection(id)

    try:
        log_db().send_info(f"Inserting new post with ID {id_collection} into channel ID {id}.")
        await telegram_channels_collection.insert_one({
            "_id": int(id_collection),
            "date": date,
            "text": text
        })

        telegram_channels_collection = info.telegram_channels
        log_db().send_info(f"Updating last_updated for channel ID {id} to {date}.")
        await telegram_channels_collection.update_one({"id": int(id)}, {"$set": {"last_updated": date}})

        log_db().send_info(f"New post created and last_updated updated successfully for channel ID {id}.")
    except Exception as e:
        log_db().send_critical(f"An error occurred while creating new post for channel ID {id}: {str(e)}")
        return None

async def return_data_last_changed_telegram_channel(id: int):
    log_db().send_info(f"Starting return_data_last_changed_telegram_channel() function for channel ID {id}.")
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.telegram_channels

    try:
        log_db().send_debug(f"Fetching last_updated for channel ID {id}.")
        result = await telegram_channels_collection.find_one({"id": id})

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
    
async def get_documents_from_telegram_channels_before_date(id: str, date: datetime):
    log_db().send_info(f"Starting get_documents_from_telegram_channels_before_date() function for channel ID {id} and date {date}.")
    client = get_url_connection()
    info = client.info
    telegram_channels_collection = info.get_collection(id)

    try:
        log_db().send_info(f"Fetching documents from channel ID {id} before date {date}.")
        if isinstance(date, datetime):
            documents = list()
            cursor = telegram_channels_collection.find({"date": {"$gte": date}})
            async for doc in cursor:
                documents.append(doc)
            log_db().send_info(f"Documents fetched successfully from channel ID {id} before date {date}.")
            return documents
        else:
            log_db().send_error("Provided date is not of type datetime.")
            return None
    except Exception as e:
        log_db().send_critical(f"An error occurred while fetching documents from channel ID {id}: {str(e)}")
        return None