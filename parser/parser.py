import logging  # стандартная библиотека для логирования
import parser_functions  # библиотека этого парсера
import os



from telethon import TelegramClient, events, sync, connection  # pip3 install telethon

from config import api_id, api_hash  # получение айди и хэша нашего приложения из файла config.py



#api_id = os.environ['API_ID']
#api_hash = os.environ['API_HASH']

# настройка логгера
logging.basicConfig(
    level=logging.INFO,
    filename='parser_log.log',
    filemode='w',
    format="%(asctime)s %(levelname)s %(message)s"
)


logging.info("script started")  # сообщение о начале работы в лог
def parse_channels(url):
    flag = True  # флаг нужен для корректного логирования результата работы парсера (успешно/неуспешно)

    logging.info(f"parsing channel {url}")  # сообщение об обрабатываемом канале в лог

    with TelegramClient('new_session', api_id, api_hash) as tc:  # запуск клиента
        try:
            err = parser_functions.parse(tc, url)  # обработка сообщений
           
            if err:  # обработка возможных ошибок и запись их в лог
                logging.warning(err)
            else:  # запись в лог об успешной работе при отсутствии ошибок
                logging.info("parsing done successfully")
                tc.disconnect()

        except Exception as ex:  # обработка критической ошибки вроде ввода некорректной ссылки на канал, или отсутствия
                                # доступа к каналу
            logging.critical(f"critical error {ex}")
            flag = False

    if flag:  # запись в лог об успешной или неуспешной работе скрипта
        logging.info("script is done successfully")
    else:
        logging.warning("some errors occurred during script execution")

parse_channels("https://t.me/kommersant18")


