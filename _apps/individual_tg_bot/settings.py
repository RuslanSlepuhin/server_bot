import os

from dotenv import load_dotenv

load_dotenv(".env")

# Параметры конфигурации тг бота
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Параметры конфигурации для PostgreSQL
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_URL = os.getenv("DB_URL")

# Параметры конфигурации для Flask
APP_HOST = os.getenv("APP_HOST")
APP_PORT = os.getenv("APP_PORT")
APP_DEBUG = os.getenv("APP_DEBUG")
