import asyncio
from telegram_chats.scraping_telegramchats2 import WriteToDbMessages

def client_init():
    client_class = WriteToDbMessages()
    asyncio.run(client_class.client_init())

if __name__ == "__main__":
    client_init()

