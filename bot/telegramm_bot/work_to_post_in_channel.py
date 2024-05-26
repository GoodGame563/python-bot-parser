from dotenv import load_dotenv
import os
import sys
import asyncio
sys.path.append(os.path.join(os.getcwd(), '..'))
from logs.loging import log_admin_bot
from data.settings_db import get_all_settings
from data.telegram_channel_db import get_telegramm_channels, exists_new_update, update_telegram_channel_last_send, get_documents_from_telegram_channels_before_date
from aiogram import Bot, Dispatcher, types, F
import aiohttp

from dateutil.relativedelta import relativedelta
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.markdown import text, bold, italic, code, pre, link
from minio_function import get_file
from aiogram.utils.media_group import MediaGroupBuilder, InputMediaPhoto
load_dotenv()

id_chanel = os.environ.get('CHAT_ID')
async def new_text(text:str):
    async with aiohttp.ClientSession() as session:
        response = await session.get('https://goodgame563.pythonanywhere.com/generate', json={"request":text})
    return await response.json()

async def print_post(bot):
    while True:
        settings = await get_all_settings()
        if not settings.get("send_post"):
            log_admin_bot().send_info("Posting is stopped")
            await asyncio.sleep(60)
            continue
        channels = await get_telegramm_channels()
        for channel in channels:
            if await exists_new_update(channel) == True:
                namechannel = channels[channel][0]
                mem = await get_documents_from_telegram_channels_before_date(str(channel), channels[channel][2])
                chat = id_chanel
                if mem is not None:
                    for document in mem:  
                        try:
                            id_message = document.get("_id")
                            if settings.get("neural_enabled"):
                                result = await new_text(document['text'])
                                document['text'] = result.get("result").replace("##", "") 
                                text_to = text(document['text'] + (link("Источник", f"{namechannel}/{id_message}") if settings.get("link_to_source") else ""))
                            else:
                                document['text'] = document['text']+"   "
                                document['text'] = document["text"][:document["text"].find("@")-1]+document["text"][document["text"].find(" ", document["text"].find("@")):-1]     
                                text_to = text(bold(document["text"].split("\n")[0])+ "\n" + "\n".join(document["text"].split('\n')[1:]) +"\n" + (link("Источник", f"{namechannel}/{id_message}" if settings.get("link_to_source") else "")))
                            count = document.get('count_img')
                            if not settings.get("posting_image"):
                                count = None
                            if count is not None:
                                    if document["url"][0].split('.')[1] == "jpg":
                                        if (int(count) == 1):
                                            file = get_file(document["url"][0])
                                            hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][0].split('/')[1])
                                            if len(text_to) > 1024:
                                                text_to = text_to.split('\n')[0] + "\n".join(text_to.split('\n')[1:-2])[0:1024-len(text_to.split('\n')[0])-len(text_to.split('\n')[-1])] + "\n" + text_to.split('\n')[-1]
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
                                        if (int(count) == 1):
                                            file = get_file(document["url"][0])
                                            #print(document["url"][0].split('/')[1])
                                            hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][0].split('/')[1])
                                            await bot.send_video(int(chat), video=hs, caption=text_to, duration=1000, supports_streaming=True, request_timeout=2000)
                            else:
                                await bot.send_message(int(chat), text_to, parse_mode=ParseMode.MARKDOWN)
                            await update_telegram_channel_last_send(channel, document["date"] + relativedelta(seconds=1))
                        except Exception as e:
                            log_admin_bot().send_error(f'Error sending {e}')
                            continue
                        await asyncio.sleep(3.5)
        await asyncio.sleep(60)