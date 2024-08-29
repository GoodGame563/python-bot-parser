import asyncio
import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))

from data.channels_db import return_channels
from data.settings_db import *
from data.sites_db import site_db
from dateutil import parser
from pprint import pprint
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dateutil.relativedelta import relativedelta  
from data.settings_db import *
from tqdm import tqdm
is_docker = os.environ.get('POST_IN_DOCKER')

hub_url = ""

if is_docker == 'True':
    hub_url = 'http://browser:4444/wd/hub'
else:
    hub_url = 'http://localhost:4444/wd/hub'

async def check_new_update(url, date: datetime):
    async with aiohttp.ClientSession() as session:
        try:
            list_items = []
            async with session.get(url) as response:
                if response.ok:
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')   
                    date_soup = soup.find('item')
                    if date_soup is None:
                        date_soup = soup.find('url')
                        if date_soup.find('pubdate') is not None:
                            date_html = date_soup.pubdate.contents[0]   
                            date_obj = parser.parse(date_html, ignoretz = True)  
                            if date_obj > date:
                                for item in soup.findAll('url'):
                                    date_obj = parser.parse(item.pubdate.contents[0], ignoretz = True) - relativedelta(hours=int(str(item.pubdate.contents[0]).split('+')[1][:2]))
                                    if date_obj > date:
                                        list_items.append(item)
                        if date_soup.find('lastmod') is not None:
                            date_html = date_soup.lastmod.contents[0]
                            date_obj = parser.parse(date_html, ignoretz = True)
                            if date_obj > date:
                                for item in soup.findAll('url'):
                                    date_obj = parser.parse(item.lastmod.contents[0], ignoretz = True) - relativedelta(hours=int(str(item.lastmod.contents[0]).split('+')[1][:2]))
                                    if date_obj > date:
                                        list_items.append(item)
                    else:
                        date_html = date_soup.pubdate.contents[0]
                        date_obj = parser.parse(date_html, ignoretz = True)
                        if date_obj > date:
                            for item in soup.findAll('item'):
                                date_obj = parser.parse(item.pubdate.contents[0], ignoretz = True) - relativedelta(hours=int(str(item.pubdate.contents[0]).split('+')[1][:2]))
                                if date_obj > date:
                                    list_items.append(item)
                else: 
                    print(f"error {url}")
                    chrome_options = webdriver.ChromeOptions()
                    driver = webdriver.Remote(command_executor=hub_url,options=chrome_options)
                    driver.get(url)
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    text = driver.find_element(By.TAG_NAME, 'body').get_attribute('outerHTML')
                    soup = BeautifulSoup(text, 'html.parser')   
                    date_soup = soup.find('item')
                    if date_soup is None:   
                        date_soup = soup.find('url')
                        if date_soup.find('pubdate') is not None:
                            date_html = date_soup.pubdate.contents[0]   
                            date_obj = parser.parse(date_html, ignoretz = True)  
                            if date_obj > date:
                                for item in soup.findAll('url'):
                                    date_obj = parser.parse(item.pubdate.contents[0], ignoretz = True) - relativedelta(hours=int(str(item.pubdate.contents[0]).split('+')[1][:2]))
                                    if date_obj > date:
                                        list_items.append(item)
                        if date_soup.find('lastmod') is not None:
                            date_html = date_soup.lastmod.contents[0]
                            date_obj = parser.parse(date_html, ignoretz = True)
                            if date_obj > date:
                                for item in soup.findAll('url'):
                                    date_obj = parser.parse(item.lastmod.contents[0], ignoretz = True) - relativedelta(hours=int(str(item.lastmod.contents[0]).split('+')[1][:2]))
                                    if date_obj > date:
                                        list_items.append(item)    
                    else:
                        date_html = date_soup.pubdate.contents[0]
                        date_obj = parser.parse(date_html, ignoretz = True)
                        if date_obj > date:
                            for item in soup.findAll('item'):
                                date_obj = parser.parse(item.pubdate.contents[0], ignoretz = True) - relativedelta(hours=int(str(item.pubdate.contents[0]).split('+')[1][:2]))
                                if date_obj > date:
                                    list_items.append(item)
                    driver.quit()
            return list_items
        except Exception as e:
            try:
                chrome_options = webdriver.ChromeOptions()
                driver = webdriver.Remote(command_executor=hub_url,options=chrome_options)
                driver.get(url)
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body')))
                text = driver.find_element(By.TAG_NAME, 'body').get_attribute('outerHTML')
                text = str(text).replace('&lt;', '<').replace('&gt;', '>')
                soup = BeautifulSoup(text, 'html.parser')   
                date_soup = soup.find('item')
                if date_soup is None:   
                    date_soup = soup.find('url')
                    if date_soup.find('pubdate') is not None:
                        date_html = date_soup.pubdate.contents[0]   
                        date_obj = parser.parse(date_html, ignoretz = True)  
                        if date_obj > date:
                            for item in soup.findAll('url'):
                                date_obj = parser.parse(item.pubdate.contents[0], ignoretz = True) - relativedelta(hours=int(str(item.pubdate.contents[0]).split('+')[1][:2]))
                                if date_obj > date:
                                    list_items.append(item)
                    if date_soup.find('lastmod') is not None:
                        date_html = date_soup.lastmod.contents[0]
                        date_obj = parser.parse(date_html, ignoretz = True)
                        if date_obj > date:
                            for item in soup.findAll('url'):
                                date_obj = parser.parse(item.lastmod.contents[0], ignoretz = True) - relativedelta(hours=int(str(item.lastmod.contents[0]).split('+')[1][:2]))
                                if date_obj > date:
                                    list_items.append(item)    
                else:
                    date_html = date_soup.pubdate.contents[0]
                    date_obj = parser.parse(date_html, ignoretz = True)
                    if date_obj > date:
                        for item in soup.findAll('item'):
                            date_obj = parser.parse(item.pubdate.contents[0], ignoretz = True) - relativedelta(hours=int(str(item.pubdate.contents[0]).split('+')[1][:2]))
                            if date_obj > date:
                                list_items.append(item)
                driver.quit()
            except Exception as e:
                print(f"Error: {e}")
            return list_items
                    


async def add_text_from_site(url:str, channel: str, items: list):
    s_db = site_db(channel)
    sites = await s_db.get_sites_by_url(url)
    key_words = sites['key_words']
    bad_words = sites['bad_words']
    print(f"\n{url}\n")
    #print(items)
    items = tqdm(items)
    for item in items:
        soup_date = BeautifulSoup(str(item), 'html.parser')
        if soup_date.find('pubdate') is not None:
            date = parser.parse(str(soup_date.pubdate.contents[0]), ignoretz = True) - relativedelta(hours=int(str(soup_date.pubdate.contents[0]).split('+')[1][:2]))
        elif soup_date.find('lastmod') is not None:
            date = parser.parse(str(soup_date.lastmod.contents[0]), ignoretz = True) - relativedelta(hours=int(str(soup_date.lastmod.contents[0]).split('+')[1][:2]))
        else:
            print(f"date not found {url}")
            break
        if item.find('loc'):
            link = item.loc.contents[0]
        else:
            link = str(item).split('<link/>')[1].split('\n')[0].split(' ')[0].split('<')[0]
        
        text = ""
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(link)
                if response.ok:
                    text = await response.text()
                elif response.status == 400 or response.status == 403:
                    repit = True
                    count_try = 0
                    while repit:
                        try:
                            count_try += 1
                            chrome_options = webdriver.ChromeOptions()
                            driver = webdriver.Remote(command_executor=hub_url,options=chrome_options)
                            driver.get(link)
                            WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, 'body')))
                            text = driver.find_element(By.TAG_NAME, 'body').get_attribute('outerHTML')
                            driver.quit()
                            repit = False
                        except:
                            print("Repit try")
                            repit = True
                            if count_try == 5:
                                repit = False
                else:
                    print(f"not work {link}")
                    continue
        except:
            repit = True
            count_try = 0
            while repit:
                try:
                    count_try += 1
                    chrome_options = webdriver.ChromeOptions()
                    driver = webdriver.Remote(command_executor=hub_url,options=chrome_options)
                    driver.get(link)
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    text = driver.find_element(By.TAG_NAME, 'body').get_attribute('outerHTML')
                    driver.quit()
                    repit = False
                except:
                    print("Repit try")
                    repit = True
                    if count_try == 5:
                        repit = False 
            
        soup = BeautifulSoup(text, 'html.parser')
        invalid_tags = ['script', 'form', 'label', 'img', 'svg', 'i', 'link', 'button', 'input', 'textarea', 'use', 'picture',]
        for tag in invalid_tags:
            for match in soup.findAll(tag):
                match.replaceWithChildren()
        count_try = 0
        final_text = ""
        while count_try < 3:
            try:
                async with aiohttp.ClientSession() as session:
                    response = await session.get('https://goodgame563.pythonanywhere.com/take_text_from_request', 
                                                    json={"request": soup.text.replace('\n', ' ').replace('  ', ' ')}, 
                                                    timeout = 100)
                    if response.ok:
                        final_text = await response.json()
                        final_text = final_text['result']
                        break
            except:
                print("Failed to get")
            finally:
                count_try += 1
        text_is_correct = await get_text_from_filters(final_text, key_words, bad_words)
        if text_is_correct: 
            await s_db.create_new_sites_parsing(id = str(sites['_id']), date=date, text = final_text, url= str(link))
        await s_db.update_date_sites(url= url, date= date)

        

async def get_text_from_filters(text:str, key_words, bad_words):
    if len(text) == 0:
        return False
    for bad in bad_words:
        if bad in text.lower():
            return False
        
    if len(key_words) == 0: 
        return True
    for good in key_words:
        if good in text.lower():
            return True
    return False

async def rss_parser():
    while True:
        channels = await return_channels()
        for channel in channels:
            set_db = setting_db(channel)
            settings = await set_db.get_all_settings()
            if not (settings).get("parser"):
                await asyncio.sleep(60)
                continue
            s_db = site_db(channel)
            sites = await s_db.get_sites()
            for site in sites:
                result = await check_new_update(site, sites[site][1])
                result.reverse()
                await add_text_from_site(site, channel, result)
        
        
        
        
        await asyncio.sleep(300)

   
