import configparser
import os
from _apps.amin_panel_tg_view.views.bot.bot_view import BotView
from _apps.talking_bot.mvp_connect_talking_bot import talking_bot_run
from invite_bot_ver2 import run as run_parser_bot
from _apps.endpoints import endpoints
from multiprocessing import Process, Pool
import settings.os_getenv as settings
# ev = Event()

num_processes = os.cpu_count()

def start_bot(double=False, token_in=None):
    # time.sleep(3)
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

def startFMCBots():
    from _apps.coffee_customer_bot_apps import main
    main.start_method()

if __name__ == "__main__":

    # start_bot(double=True, token_in=settings.token_red)

    p1 = Process(target=start_endpoints, args=())
    p2 = Process(target=start_bot, args=())
    p3 = Process(target=start_bot, args=(True, settings.token_red))
    p4 = Process(target=talking_bot_run, args=())
    p5 = Process(target=start_admin_panel, args=())

    p1.start()
    p4.start()
    p2.start()
    p3.start()
    p5.start()

    # start_bot(double=True, token_in=settings.token_red)

    # p1.join()
    # p2.join()
    # p3.join()


