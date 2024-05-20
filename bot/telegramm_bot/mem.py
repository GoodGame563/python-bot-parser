import asyncio
from aiogram.types import InputFile, FSInputFile
from aiogram.methods.send_media_group import SendMediaGroup
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, or_f, Command
from aiogram.utils.chat_action import ChatActionSender
import os
import sys
import urllib
from kbds import reply
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.utils.media_group import MediaGroupBuilder, InputMediaPhoto
from dateutil.relativedelta import relativedelta  # pip3 install python-dateutil
from minio_function import get_file
import datetime
sys.path.append(os.path.join(os.getcwd(), '..'))
from data.telegram_channel_db import get_documents_from_telegram_channels_before_date

bot = Bot(token='7064443400:AAGYVAtnIDmJRGEnZ89hzzqjYvKJV5zNAZI')
chat = -1002096816791
oldest =  datetime.datetime.strptime("1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
namechannel = "@kommersant18"
dp = Dispatcher()
@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("Привет, я бот для настройки бота-агрегатора новостей.", reply_markup= reply.main_menu_markup)
   
    mem = get_documents_from_telegram_channels_before_date("2032566955", oldest)
    if mem is not None:
        for document in mem:
            text_to = text(bold(document["text"].split("\n")[0])+ "\n" + "\n".join(document["text"].split('\n')[1:]) +"\n" + f"Источник {namechannel}")
            print(text_to)
            count = document.get('count_img')
            if count is not None:
                try:
                    if document["url"][0].split('.')[1] == "jpg":
                        if (int(count) == 1):
                            file = get_file(document["url"][0])
                            hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][0].split('/')[1])
                            if len(text_to) > 1024:
                                text_to = text_to.split('\n')[0] + "\n".join(text_to.split('\n')[1:-2])[0:1024-len(text_to.split('\n')[0])-len(text_to.split('\n')[-1])] + "\n" + text_to.split('\n')[-1]
                                print(text_to)
                            await bot.send_photo(int(chat), hs, caption=text_to, request_timeout=1000, parse_mode=ParseMode.MARKDOWN)
                        else:
                            medias = []
                            for i in range(int(count)): 
                                if i == 1:
                                    file = get_file(document["url"][i])
                                    hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][i].split('/')[1])
                                    if len(text_to) > 1024:
                                        text_to = text_to.split('\n')[0] + "\n".join(text_to.split('\n')[1:-2])[0:1024-len(text_to.split('\n')[0])-len(text_to.split('\n')[-1])] + "\n" + text_to.split('\n')[-1]
                                    media = InputMediaPhoto(media=hs, caption=text_to, parse_mode=ParseMode.MARKDOWN)
                                    medias.append(media)
                                else:
                                    file = get_file(document["url"][i])
                                    hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][i].split('/')[1])
                                    media = InputMediaPhoto(media=hs)
                                    medias.append(media)
                            await bot.send_media_group(chat_id = chat, media=medias, request_timeout=1000)
                    else:
                        print("video")
                        if (int(count) == 1):
                            file = get_file(document["url"][0])
                            #print(file)
                            print(document["url"][0].split('/')[1])
                            hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][0].split('/')[1])
                            #video = FSInputFile("source.mp4", filename=document["url"][0].split('/')[1])
                            await bot.send_video(int(chat), video=hs, caption=text_to, duration=300, supports_streaming=True, request_timeout=1000)
                except:
                    continue
            else:
                await bot.send_message(int(chat), text_to)
            await asyncio.sleep(3.5)


async def main():
    await dp.start_polling(bot)

asyncio.run(main())