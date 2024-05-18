import logging



class log_admin_bot():

    def __init__(self):
        self.admin_bot_logger = logging.getLogger('admin_bot')
        self.admin_bot_logger.setLevel(logging.DEBUG)
        ch = logging.FileHandler('admin_bot_log.log', 'w')
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.admin_bot_logger.addHandler(ch)

    def send_message(self, message: str):
        print("adsjkfdskjdfjk")
        self.admin_bot_logger.info(msg=message)

log_admin_bot().send_message(message="huy")