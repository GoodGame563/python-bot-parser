from telethon import TelegramClient
from dotenv import load_dotenv
from os import environ

load_dotenv()

api_id = environ.get('API_ID')
api_hash = environ.get('API_HASH')
phone_number = environ.get('PHONE_NUMBER')

if api_id is None or api_hash is None or phone_number is None:
    assert False

client = TelegramClient("test_session", api_id=api_id, api_hash=api_hash,device_model='Samsung Galaxy S20 FE, running Android 13', system_version='4.16.30-vxCUSTOM', app_version='1.0.1',)

assert client.connect()

client.send_code_request(phone_number)

me = client.sign_in(phone_number, input('Enter code: '))