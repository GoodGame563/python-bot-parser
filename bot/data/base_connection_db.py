import os
import datetime
import sys
from dotenv import load_dotenv
sys.path.append(os.path.join(os.getcwd(), '..'))
import motor.motor_asyncio
from logs.loging import log_db


load_dotenv()

url_connection_out = os.environ.get('DATA_DB_URL')
url_connection_in = os.environ.get('DB_CONTAINER_NAME')

root_user = os.environ.get('DATA_DB_ROOT_USER')
root_password = os.environ.get('DATA_DB_ROOT_PASS')

port_in = os.environ.get('DATA_DB_PORT_CONTAINER')
port_out = os.environ.get('DATA_DB_PORT_DESKTOP')

is_docker = os.environ.get('POST_IN_DOCKER')



def get_url_connection():
    if(url_connection_out is None):
        log_db().send_critical('Could not connect to database, Error: url_connection is none')
        return None
    if(root_user is None):
        log_db().send_critical('Could not connect to database, Error: root_user is none')
        return None
    if(root_password is None):
        log_db().send_critical('Could not connect to database, Error: root_password is none')
        return None
    if(port_in is None):
        log_db().send_critical('Could not connect to database, Error: port is none')
        return None
    if is_docker == 'True':
        client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{root_user}:{root_password}@{url_connection_in}:{port_in}/")
    else:
        client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{root_user}:{root_password}@{url_connection_out}:{port_out}/")
    return client

async def check_exist_database_if_create():
    log_db().send_info("Starting check_exist_database_if_create() function.")

    needs_paser = os.environ.get("NEED_SITES_CUSTOM_PARSER") == 'True'
    need_special_words = os.environ.get('NEED_SPECIAL_WORDS') == 'True'

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
    sites_collection = list()
    special_words = list()

    if needs_paser:
        sites_url = os.environ.get('DEFAULT_VALUES_SITES') 
        if sites_url is not None:
            sites_url = sites_url.replace(" ","").split(",")
        words = os.environ.get('DEFAULT_SPECIAL_WORDS') 
        if  words is not None:
            words =  words.replace(" ","").split(",")
        for site in sites_url:
            sites_collection.append({
                "url": site,
                "last_updated": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z"),
                "last_send": datetime.datetime.strptime("1970-01-01 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
            })
        for word in words:
            special_words.append({
                "word": word
            })   


    client = get_url_connection()
    info = client.info
    telegram_channels_table = info.telegram_channels

    try:
        if needs_paser:
            url_sites = info.url_sites
            if await url_sites.estimated_document_count() != 0:
                log_db().send_info("Url sites already exist in the database.")
            else:
                await url_sites.insert_many(sites_collection)
                if need_special_words:
                    log_db().send_debug("Inserting default special words into the database.")
                    await info.special_words.insert_many(special_words)
        if await telegram_channels_table.estimated_document_count() != 0:
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
            if await key_words_collection.estimated_document_count() == 0:
                log_db().send_debug("Inserting default key words into the database.")
                await key_words_collection.insert_many(words_collection)
            else:
                log_db().send_info("Key words already exist in the database.")

        if await telegram_channels_table.estimated_document_count() == 0:
            log_db().send_debug("Inserting default telegram channels into the database.")
            await telegram_channels_table.insert_many(telegram_channels_collection)

        log_db().send_info("Database check and setup completed successfully.")
    except Exception as e:
        log_db().send_critical(f"An error occurred: {str(e)}")
        return None
   
async def set_basic_parameters():
    log_db().send_info("Starting set_basic_parameters() function.")
    client = get_url_connection()
    info = client.info
    settings = info.settings
    is_posting_image = bool(os.environ.get('POST_IMAGE') == 'True')
    is_to_create_link_to_source = bool(os.environ.get('LINK_TO_SOURCE') == 'True')
    parser_enabled = bool(os.environ.get('POST_IMAGE') == 'True')
    send_post_enabled = bool(os.environ.get('LINK_TO_SOURCE') == 'True')
    neural_enabled = bool(os.environ.get('NEURAL_NETWORK_ENABLED') =='True')
    need_paser = os.environ.get("NEED_SITES_CUSTOM_PARSER") == 'True'
    need_special_words = os.environ.get('NEED_SPECIAL_WORDS') == 'True'
    if await settings.estimated_document_count() == 0 and is_posting_image is not None and is_to_create_link_to_source is not None:
        work_on_time_enabled = bool(os.environ.get('WORK_ON_TIME_ENABLED') == 'True') if (os.environ.get('WORK_ON_TIME_ENABLED') is not None) else False
        if work_on_time_enabled:
            start_time = datetime.datetime.strptime(os.environ.get('START_TIME'), "%H:%M:%S")
            end_time = datetime.datetime.strptime(os.environ.get('END_TIME'), "%H:%M:%S")
            result = await settings.insert_one({"_id":1,"posting_image": bool(is_posting_image), "link_to_source":bool(is_to_create_link_to_source), "start_time":start_time, "end_time":end_time, "work_on_time": bool(work_on_time_enabled),"parser": parser_enabled, "send_post": send_post_enabled, "neural_enabled":  neural_enabled, "web_paser": need_paser, "need_special_words": need_special_words})
            log_db().send_info(f"Basic parameters were set successfully. {result}")
            return result
        else:
            result = await settings.insert_one({"_id":1,"posting_image": bool(is_posting_image), "link_to_source":bool(is_to_create_link_to_source), "work_on_time": bool(work_on_time_enabled),"parser": parser_enabled, "send_post": send_post_enabled, "neural_enabled":  neural_enabled, "web_paser": need_paser, "need_special_words": need_special_words})
            log_db().send_info(f"Basic parameters were set successfully. {result}")
            return result