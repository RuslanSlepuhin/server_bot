import configparser
import os
from _apps.amin_panel_tg_view.views.bot.bot_view import BotView
from _apps.talking_bot.mvp_connect_talking_bot import talking_bot_run
from invite_bot_ver2 import run as run_parser_bot
from _apps.endpoints import endpoints
from multiprocessing import Process, Pool
import settings.os_getenv as settings
from _apps.coffee_customer_bot_apps.coffee_customer_bot.coffee_customer_bot import CustomerBot
from _apps.coffee_customer_bot_apps.coffee_horeca_bot.coffee_horeca_bot import HorecaBot
from _apps.coffee_customer_bot_apps.endpoints.endpoints import Endpoints
from _apps.chat.bot_tg import ChatBot

config_FCM = configparser.ConfigParser()
config_FCM.read('_apps/coffee_customer_bot_apps/settings/config.ini')

customer_token = config_FCM['Bot']['customer_token']
horeca_token = config_FCM['Bot']['horeca_token']
horeca_bot = HorecaBot(horeca_token)
customer_bot = CustomerBot(customer_token)

num_processes = os.cpu_count()

def start_bot(double=False, token_in=None):
    print('main_bot is starting')
    run_parser_bot(
        double=double,
        token_in=token_in
    )
    print('bot has been stopped')

def start_endpoints():
    print('endpoints are starting')
    endpoints.run_endpoints()

def start_admin_panel():
    print('admin panel is starting')
    config = configparser.ConfigParser()
    config.read("_apps/amin_panel_tg_view/settings/config.ini")
    __token = config['Bot']['token']

    bot = BotView(token=__token)
    bot.handlers()

# ---------- FCM -----------
def start_customer_bot_FCM():
    customer_bot.bot_handlers()

def start_horeca_bot_FCM():
    horeca_bot.bot_handlers()

def start_endpoints_FCM():
    ep = Endpoints(customer_bot, horeca_bot)
    ep.main_endpoints()

def start_chat():
    chat = ChatBot()
    chat.bot_handlers()

if __name__ == "__main__":

    p1 = Process(target=start_endpoints, args=())
    p2 = Process(target=start_bot, args=())
    p3 = Process(target=start_bot, args=(True, settings.token_red))
    p4 = Process(target=talking_bot_run, args=())
    p5 = Process(target=start_admin_panel, args=())
    p6 = Process(target=start_customer_bot_FCM, args=())
    p7 = Process(target=start_horeca_bot_FCM, args=())
    p8 = Process(target=start_endpoints_FCM, args=())
    # p9 = Process(target=start_chat, args=())


    p1.start()
    p4.start()
    p2.start()
    p3.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    # p9.start()
