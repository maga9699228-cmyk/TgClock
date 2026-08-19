"""
    Main module. Contains a sheduler that sets cron job
    and run function that updates username when minute is changed.
"""
from datetime import datetime
import pytz

import asyncio
from telethon.sync import TelegramClient
from telethon import functions, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHTTPRequestHandler)
    server.serve_forever()



from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHTTPRequestHandler)
    server.serve_forever()



def time_to_string(dt: datetime) -> str:
    """
    Converts datetime object to time.
    :param datetime dt: datetime object to convert
x    :return: formatted time like '<10:41>'
    :rtype: str
    """
    hours = str(dt.hour)
    if dt.hour < 10:
        hours = "0" + hours

    minutes = str(dt.minute)
    if dt.minute < 10:
        minutes = "0" + minutes

    return f"<{hours}:{minutes}>"

async def update_clock(client: TelegramClient) -> None:
    """
    Updates clock in tg last_name
    """
    async with client as client:
        await client(functions.account.UpdateProfileRequest( 
            last_name=time_to_string(datetime.now()),
        ))

client = TelegramClient("Clock in name", config.API_ID, config.API_HASH)

async def main():
    await client.start()
    threading.Thread(target=run_web_server, daemon=True).start()

    loop = asyncio.get_running_loop()
    sheduler = AsyncIOScheduler(event_loop=loop, timezone=pytz.timezone('Asia/Vladivostok'))
    sheduler.add_job(update_clock, 'cron', minute='*', args=[client])
    sheduler.start()
    
    await update_clock(client)
    print("Скрипт успешно запущен и обновляет время!")
    
    # Заменяем упавший метод на этот бесконечный цикл:
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())
