import datetime
from data.base_connection_db import get_url_connection

from logs.loging import log_db
class setting_db(): 
    def __init__(self, name: str):
        self.name = name

    async def get_all_settings(self):
        try:
            client = get_url_connection()
            info = client[self.name]
            settings = info.settings  
            return await settings.find_one()
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None

    async def switch_mode_parser(self, mode: bool):
        try:
            client  = get_url_connection()
            info = client[self.name]
            settings = info.settings  
            await settings.update_one({ },{'$set':{'parser':bool(mode)}})
        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None

    async def switch_mode_send_post(self, mode: bool):
        try:
            client  = get_url_connection()
            info = client[self.name]
            settings = info.settings  
            await settings.update_one({ },{'$set':{'send_post':bool(mode)}})

        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None

    async def turn_on_work_on_time(self, start_time: datetime.datetime.time, end_time: datetime.datetime.time):
        try:
            client  = get_url_connection()
            info = client[self.name]
            settings = info.settings  
            await settings.update_one({},{'$set': {'work_on_time':True}})
            await settings.update_one({ },{'$set': {'start_time':start_time}})
            await settings.update_one({ },{'$set': {'end_time':end_time}})

        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None

    async def turn_off_work_on_time(self):
        try:
            client  = get_url_connection()
            info = client[self.name]
            settings = info.settings  
            await settings.update_one({},{'$set': {'work_on_time':False}})

        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None

    async def switch_mode_send_image(self, mode: bool):
        try:
            client  = get_url_connection()
            info = client[self.name]
            settings = info.settings  
            await settings.update_one({},{'$set':{'posting_image':bool(mode)}})

        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None

    async def switch_mode_send_links(self, mode: bool):
        try:
            client  = get_url_connection()
            info = client[self.name]
            settings = info.settings  
            await settings.update_one({},{'$set':{'link_to_source':bool(mode)}})

        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None

    async def switch_mode_neural_network(self, mode: bool):
        try:
            client  = get_url_connection()
            info = client[self.name]
            settings = info.settings  
            await settings.update_one({},{'$set':{'neural_enabled':bool(mode)}})

        except Exception as e:
            log_db().send_critical(f"An error occurred: {str(e)}")
            return None