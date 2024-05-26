import logging
from logging.handlers import RotatingFileHandler

class log_default():
    def send_info(self, message: str):
        self.logger.info(msg=message)
    def send_debug(self, message: str):
        self.logger.debug(msg=message)
    def send_warning(self, message: str):
        self.logger.warning(msg=message)
    def send_error(self, message: str):
        self.logger.error(msg=message)
    def send_critical(self, message: str):
        self.logger.error(msg=message)

class log_admin_bot(log_default):
    def __init__(self,  create = False):
        self.logger = logging.getLogger('admin_bot')
        if self.logger.handlers == [] or create:
            self.logger.setLevel(logging.DEBUG)
            handler = RotatingFileHandler('../logs/admin_bot_log.log', maxBytes=20000, backupCount=0, mode='w', encoding="utf-8")
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
    
class log_parser_bot(log_default):
    def __init__(self, create = False):
        self.logger = logging.getLogger('parser_bot')
        if self.logger.handlers == [] or create:
            self.logger.setLevel(logging.DEBUG)
            handler = RotatingFileHandler('../logs/parser_bot_log.log', maxBytes=20000, backupCount=0, mode='w', encoding="utf-8")
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)

class log_db(log_default):
    def __init__(self, create = False):
        self.logger = logging.getLogger('db')
        if self.logger.handlers == [] or create:
            self.logger.setLevel(logging.INFO)
            handler = RotatingFileHandler('../logs/db_log.log', maxBytes=20000, backupCount=0, mode='w', encoding="utf-8")
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(handler)
