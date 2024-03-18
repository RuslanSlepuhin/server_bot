import asyncio
import configparser

from telethon import TelegramClient

from telegram_chats.scraping_telegramchats2 import WriteToDbMessages

def client_init():
    client_class = WriteToDbMessages()
    asyncio.run(client_class.client_init())

def admin_panel_init():
    config = configparser.ConfigParser()
    config.read("./_apps/amin_panel_tg_view/settings/config.ini")

    api_id = config['Telegram_api']['api_id']
    api_hash = config['Telegram_api']['api_hash']
    username = config['Telegram_api']['username']

    client = TelegramClient(username, int(api_id), api_hash)
    client.start()
    print("connection done")
    client.disconnect()
    print("disconnect")


if __name__ == "__main__":
    # client_init()
    admin_panel_init()

