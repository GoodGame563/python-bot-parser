import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.join(os.getcwd(), '..'))
import motor.motor_asyncio
from logs.loging import log_db
from datetime import datetime


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
    client = get_url_connection()
    info = client.info
    settings = info.settings
    if await settings.estimated_document_count() > 0:
        await settings.find_one_and_delete({"_id": int(1)})
    if await settings.estimated_document_count() == 0:
        await settings.insert_one({
            "work_all": True,
            "work_on_time_all": False,
            "all_turn_on_time": datetime.strptime("09:00:00", "%H:%M:%S"),
            "all_turn_off_time": datetime.strptime("21:00:00", "%H:%M:%S")
        })
    
