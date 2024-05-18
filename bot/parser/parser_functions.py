
import time
from telethon.tl.types import MessageEntityTextUrl
from dateutil.relativedelta import relativedelta  # pip3 install python-dateutil

import datetime
import os
import sys
import shutil

sys.path.append(os.path.join(os.getcwd(), '..'))
from data.db import create_new_channel_parsing
from data.db import return_data_last_changed_collection
from data.db import add_image, get_key_words, check_post_exist, update_data
from minio_function import add_file

main_folder = "record"

def get_text_from_filters(text):
    words = get_key_words()
    if len(words) == 0: 
        return True
    for id_word in words:
        if words[id_word] in text:
            return True
    return False



def get_channel_id(client, link):  # получение ID канала
    m = client.get_messages(link, limit=1)
    channel_id = m[0].peer_id.channel_id
    return str(channel_id)


def clearify_text(msg):  # очищение текста от символов гиперссылки
    text = msg.message
    find_int_dog = text.find('@')
    if find_int_dog != -1:
        print("find")
        find_int_end_word = text.find(' ',  find_int_dog)
        text = text[:find_int_dog] + text[find_int_end_word+1:]

    #text_splitted = text.split()
    #text_listed = [word for word in text_splitted if word != ' ']
    #return " ".join(text_listed)
    return text

def get_image(client, msg, channel_name, directory_name):
    if msg.media:
        data = client.download_media(msg, f"{main_folder}/{channel_name}/{directory_name}")
       
        return f"{channel_name}/{msg.id}.{data.split(".")[1]}"


def get_message_content(client, msg, url, channel_name, directory_name):  
    msg_date = str(msg.date) 
    msg_url = url + '/' + str(msg.id)  
    file = open(f"{main_folder}/{channel_name}/{directory_name}/{directory_name}_meta.txt", 'a+')  
    file.write(msg_url)
    file.write('\n' + msg_date)
    file.close()

    if msg.message: 
        with open(f"{main_folder}/{channel_name}/{directory_name}/{directory_name}.txt", "w", encoding='utf-8') as document:
            text = clearify_text(msg=msg)
            create_new_channel_parsing(channel_name, msg.date, text, 0, msg.id)
            document.write(text)
            document.write('\n')
            document.close()
    if msg.media:  
        client.download_media(message=msg, file=f"{main_folder}/{channel_name}/{directory_name}")
    if msg.entities:  
        urls = [ent.url for ent in msg.entities if isinstance(ent, MessageEntityTextUrl)]
        file = open(f"{main_folder}/{channel_name}/{directory_name}/{directory_name}.txt", mode='a+')
        for u in urls:
            file.write('\n' + u)
        file.close()


def find_last_parsed_date(id:int): 
    oldest = datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    temp = oldest
    oldest = return_data_last_changed_collection(int(id))
    if temp == oldest:
        oldest = datetime.datetime.now() - relativedelta(months=3)  # если сообщений нет, офсет устанавливается на                                                   # три месяца от текущей даты
    return oldest
        

def parse(client, url): 
    err = []  
    channel_id = get_channel_id(client, url)  
    time.sleep(1)
    oldest = find_last_parsed_date(int(channel_id))
    oldest += relativedelta(seconds=1) 
    for message in client.iter_messages(url, reverse=True, offset_date=oldest):
        try:
            directory_name = str(message.id) 
            if message.message:
                if (get_text_from_filters(message.message)):
                    create_new_channel_parsing(channel_id, message.date, clearify_text(message), message.id)
                else:
                    update_data(channel_id, message.date)
            if message.media:
                if(check_post_exist(channel_id, datetime.datetime.strptime(message.date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))):
                    url_path = get_image(client, message, channel_id, directory_name)
                    if (add_image(channel_id, url_path, datetime.datetime.strptime(message.date.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))):
                        #print(os.path.getsize(f"{url_path}"))
                        add_file(url_path.split('/')[1], channel_id, f"{main_folder}/{url_path}")
                else:
                    update_data(channel_id, message.date)
        except Exception as passing: 
            err.append(passing)
            continue
        if (os.path.isdir(f"{main_folder}/{channel_id}")): 
            shutil.rmtree(f"{main_folder}/{channel_id}")

    return err 
 