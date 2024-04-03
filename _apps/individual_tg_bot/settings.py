import configparser
import os

# from dotenv import load_dotenv
#
# load_dotenv("config.ini")
#
# Параметры конфигурации тг бота
# TOKEN = os.getenv("TOKEN")
# ADMIN_ID = os.getenv("ADMIN_ID")
#
# Параметры конфигурации для PostgreSQL
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_URL = os.getenv("DB_URL")
#
# # Параметры конфигурации для Flask
# APP_HOST = os.getenv("APP_HOST")
# APP_PORT = os.getenv("APP_PORT")
# APP_DEBUG = os.getenv("APP_DEBUG")
#
config = configparser.ConfigParser()
config.read("./_apps/individual_tg_bot/config.ini")
TOKEN = config["INDIVIDUAL_TG_BOT"]["TOKEN"]
DB_NAME = config["INDIVIDUAL_TG_BOT"]["DB_NAME"]
DB_USER = config["INDIVIDUAL_TG_BOT"]["DB_USER"]
DB_PASSWORD = config["INDIVIDUAL_TG_BOT"]["DB_PASSWORD"]
DB_HOST = config["INDIVIDUAL_TG_BOT"]["DB_HOST"]
DB_PORT = config["INDIVIDUAL_TG_BOT"]["DB_PORT"]
DB_URL = config["INDIVIDUAL_TG_BOT"]["DB_URL"]

# Параметры конфигурации для Flask
APP_HOST = config["INDIVIDUAL_TG_BOT"]["APP_HOST"]
APP_PORT = config["INDIVIDUAL_TG_BOT"]["APP_PORT"]
APP_DEBUG = config["INDIVIDUAL_TG_BOT"]["APP_DEBUG"]

