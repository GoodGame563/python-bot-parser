from dotenv import load_dotenv
import os
import sys
import asyncio
sys.path.append(os.path.join(os.getcwd(), '..'))
from logs.loging import log_admin_bot
from data.settings_db import *
from data.telegram_channel_db import *
from data.channels_db import *
from data.sites_db import site_db
from aiogram import types, F
import aiohttp

from dateutil.relativedelta import relativedelta
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.markdown import text, bold, link
from data.minio_function import get_file, check_file_size
from aiogram.utils.media_group import InputMediaPhoto
load_dotenv()

async def new_text(text:str):
    async with aiohttp.ClientSession() as session:
        response = await session.get('https://goodgame563.pythonanywhere.com/generate', json={"request":text})
    return await response.json()

async def send_site(site, sites, bot, send_channel, s_db, settings):
    rofl = await s_db.get_documents_from_telegram_channels_before_date(str(sites[site][3]), sites[site][2])
    chat = send_channel
    for doc in rofl:
        try:
            id_message = doc.get("id")
            if (id_message).find(":",7) != -1:
                id_message = id_message[:str(id_message).find(":",7)] + id_message[str(id_message).find(":",7)+1:]
                
            text_to = text(doc["text"] + (("\n" + link("Источник", f"{id_message}")) if settings.get("link_to_source") else ""))
            #print(text_to)
            await bot.send_message(int(chat), text_to.replace("**", "*").replace("##", "").replace("\\*", "*"), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
            await s_db.update_sites_last_send(site, doc["date"] + relativedelta(seconds=1))
            await asyncio.sleep(1.5)
        except Exception as e:
            log_admin_bot().send_error(f'Error sending {e}  to {id_message} in {sites[site][2]}')

async def send_channel_post(channel, channels, send_channel, tg_db, settings, bot):
    if await tg_db.exists_new_update(channel) == True:
        namechannel = channels[channel][0]
        mem = await tg_db.get_documents_from_telegram_channels_before_date(str(channel), channels[channel][2])
        chat = send_channel
        if mem is not None:
            for document in mem:  
                try:
                    id_message = document.get("_id")
                    if settings.get("neural_enabled"):
                        if len(str(document["text"])) > 50:
                            result = await new_text(document['text'])
                            document['text'] = str(result.get("result")).replace("##", "").replace("**", "*") 
                        text_to = document['text'] + text("\n"+(link("Источник", f"{namechannel}/{id_message}") if settings.get("link_to_source") else ""))
                        text_to = text_to.replace("\\.",".").replace("\\-", "-").replace("\\!","!").replace("\\=","=")
                    else:
                        document['text'] = document['text']+"   "
                        document['text'] = document["text"][:document["text"].find("@")-1]+document["text"][document["text"].find(" ", document["text"].find("@")):-1]     
                        text_to = text(bold(document["text"].split("\n")[0])+ "\n" + "\n".join(document["text"].split('\n')[1:]) +"\n" + (("\n" + link("Источник", f"{namechannel}/{id_message}")) if settings.get("link_to_source") else ""))
                        text_to = text_to.replace("\\.",".").replace("\\-", "-").replace("\\!","!").replace("\\=","=")
                    count = document.get('count_img')
                    if not settings.get("posting_image"):
                        count = None
                    if count is not None:
                            if document["url"][0].split('.')[1] == "jpg":
                                if (int(count) == 1):
                                    file = await get_file(document["url"][0])
                                    hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][0].split('/')[1])
                                    if len(text_to) > 1024:
                                        text_to = text_to.split('\n')[0] + "\n".join(text_to.split('\n')[1:-2])[0:1024-len(text_to.split('\n')[0])-len(text_to.split('\n')[-1])] + "\n" + text_to.split('\n')[-1]
                                    await bot.send_photo(int(chat), hs, caption=text_to, request_timeout=1000, parse_mode=ParseMode.MARKDOWN)
                                else:
                                    medias = []
                                    for i in range(int(count)): 
                                        if i == 1:
                                            file = await get_file(document["url"][i])
                                            hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][i].split('/')[1])
                                            if len(text_to) > 1024:
                                                text_to = text_to.split('\n')[0] + "\n".join(text_to.split('\n')[1:-2])[0:1024-len(text_to.split('\n')[0])-len(text_to.split('\n')[-1])] + "\n" + text_to.split('\n')[-1]
                                            media = InputMediaPhoto(media=hs, caption=text_to, parse_mode=ParseMode.MARKDOWN)
                                            medias.append(media)
                                        else:
                                            file = await get_file(document["url"][i])
                                            hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][i].split('/')[1])
                                            media = InputMediaPhoto(media=hs)
                                            medias.append(media)
                                    await bot.send_media_group(chat_id = chat, media=medias, request_timeout=1000)
                            else:
                                result_size_file = await check_file_size(document["url"][0])
                                if (int(count) == 1 and result_size_file):
                                    file = await get_file(document["url"][0])
                                    hs = types.input_file.BufferedInputFile(file= file, filename= document["url"][0].split('/')[1])
                                    await bot.send_video(int(chat), video=hs, caption=text_to, duration=1000, supports_streaming=True, request_timeout=2000, parse_mode=ParseMode.MARKDOWN)
                                else:
                                    await bot.send_message(int(chat), text_to, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                    else:
                        await bot.send_message(int(chat), text_to, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                    await tg_db.update_telegram_channel_last_send(channel, document["date"] + relativedelta(seconds=1))
                    await asyncio.sleep(3.5)
                except Exception as e:
                    log_admin_bot().send_error(f'Error sending {e} tp {document["date"]} chanel {namechannel} id {id_message}')
                    continue
                
async def print_post(bot):
    await asyncio.sleep(1)
    while True:
        for send_channel in await return_channels():
            set_db = setting_db(send_channel)
            tg_db = telegram_db(send_channel)
            s_db = site_db(send_channel)
            settings = await set_db.get_all_settings()
            if not settings.get("send_post"):
                log_admin_bot().send_info("Posting is stopped")
                continue
            sites = await s_db.get_sites()
            tasks = []
            for site in sites:
                tasks.append(asyncio.create_task(send_site(site, sites, bot, send_channel, s_db, settings)))
                
            channels = await tg_db.get_telegramm_channels()
            for channel in channels:
                tasks.append(asyncio.create_task(send_channel_post(channel, channels, send_channel, tg_db, settings, bot)))
            await asyncio.gather(*tasks)
        await asyncio.sleep(300)