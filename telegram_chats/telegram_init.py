import configparser
from telethon import TelegramClient

config = configparser.ConfigParser()
config.read("./settings/config.ini")


async def client_init():
    config.read("./settings/config_keys.ini")
    username = config["Telegram_double"]["username"]
    api_id = config["Telegram_double"]["api_id"]
    api_hash = config["Telegram_double"]["api_hash"]
    client = TelegramClient(username, int(api_id), api_hash)
    await client.start()
    print("connection done")
    client.disconnect()
    print("disconnect")

