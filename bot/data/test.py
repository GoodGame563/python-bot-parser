import asyncio
from telegram_channel_db import telegram_db 
async def main():
    tg_db = telegram_db("-1002179674667")
    print(await tg_db.get_telegramm_channels())

    


    

asyncio.run(main()) 