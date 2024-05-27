import asyncio
import configparser
import os
import subprocess
from _apps.amin_panel_tg_view.views.bot.bot_view import BotView
# from _apps.coffee_customer_bot_apps.coffee_horeca_bot.coffee_horeca_bot_NEW import HorecaBot
# from _apps.talking_bot.mvp_connect_talking_bot import talking_bot_run
from _apps.web_form_bot.bot_webhooks import bot_init
from invite_bot_ver2 import run as run_parser_bot
from _apps.endpoints import endpoints
from multiprocessing import Process, Pool
import settings.os_getenv as settings
from _apps.coffee_customer_bot_apps.coffee_customer_bot.coffee_customer_bot import CustomerBot
from _apps.coffee_customer_bot_apps.coffee_horeca_bot.coffee_horeca_bot_NEW import HorecaBot
# from _apps.coffee_customer_bot_apps.endpoints.endpoints import Endpoints
from _apps.chat.bot_tg import ChatBot
from _apps.coffee_customer_bot_apps.back_server_side.back_server_side import BackServer
from telegram_chats.telegram_init import client_init
from _debug import debug

from report.reports import Reports
# from sites._scraping_remotejob import RemoteJobGetInformation
# from sites.scraping_careerjet import СareerjetGetInformation
# from sites.scraping_dev import DevGetInformation
# from sites.scraping_epam_anywhere import EpamGetInformation
# from sites.scraping_habr import HabrGetInformation
# from sites.scraping_hh import HHGetInformation
# from sites.scraping_hh_it import HHITGetInformation
# from sites.scraping_hhkz import HHKzGetInformation
# from sites.scraping_geekjob import GeekGetInformation
# from sites.scraping_otta import OttaGetInformation
# from sites.scraping_praca import PracaGetInformation
# from sites.scraping_remocate import RemocateGetInformation
# from sites.scraping_wellfound import WellFoundGetInformation
# from sites.scrapping_finder import FinderGetInformation
# from utils.additional_variables.additional_variables import valid_professions
# import psutil

report = Reports()
config_FCM = configparser.ConfigParser()
config_FCM.read('_apps/coffee_customer_bot_apps/settings/config.ini')

# customer_token = config_FCM['Bot']['customer_token']
# horeca_token = config_FCM['Bot']['horeca_token']
# horeca_bot = HorecaBot()
# customer_bot = CustomerBot(customer_token)

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
    pass
    # customer_bot.bot_handlers()

def start_horeca_bot_FCM():
    h = HorecaBot()
    h.bot_handlers()

def start_endpoints_FCM():
    pass
    # ep = Endpoints(horeca_bot, customer_bot)
    # ep.main_endpoints(customer_bot, horeca_bot)

def start_chat():
    chat = ChatBot()
    chat.bot_handlers()
    # pass

def start_webForm_bot():
    bot_init()
    # pass

def form_app_start():
    command = 'python _apps/webForm/manage.py runserver'
    process = subprocess.Popen(command, shell=True)
    process.communicate()

def simpleatom_start():
    command = 'python _apps/simpleatom/manage.py runserver'
    process = subprocess.Popen(command, shell=True)
    process.communicate()

def auth_start():
    # pass
    command = 'python _apps/itcoty_web/manage.py runserver 9000'
    process = subprocess.Popen(command, shell=True)
    process.communicate()


def mock_server_FCM():
    bs = BackServer()
    bs.main_back_server()

def telegram_init_method():
    asyncio.run(client_init())

def start_individ_bot():
    from _apps.individual_tg_bot import main
    # pass

def start_flask_endpoints_indiv_bot():
    # from _apps.individual_tg_bot import flask_endpoint
    pass

def start_parser_automatically():
    from parsers.run_parsers import common_run_parsers
    common_run_parsers()

# def start_hh_parser():
#     asyncio.run(HHGetInformation(report=report).get_content(words_pattern=valid_professions))
#
# def start_other_parsers():
#     asyncio.run(all_parsers())
#
# async def all_parsers():
#     # await HHKzGetInformation(report=report).get_content(words_pattern=valid_professions)
#     await GeekGetInformation(report=report).get_content()
#     await EpamGetInformation(report=report).get_content(words_pattern=valid_professions)
#     await DevGetInformation(report=report).get_content(words_pattern=valid_professions)
#     await СareerjetGetInformation(report=report).get_content(words_pattern=valid_professions)
#     await HabrGetInformation(report=report).get_content()
#     await FinderGetInformation(report=report).get_content(words_pattern=valid_professions)
#     await PracaGetInformation(report=report).get_content(words_pattern=valid_professions)
#     await RemocateGetInformation(report=report).get_content()
#     await HHITGetInformation(report=report).get_content(words_pattern=valid_professions)
#     await RemoteJobGetInformation(report=report).get_content()
#     await OttaGetInformation(report=report).get_content()
#     await WellFoundGetInformation(report=report).get_content()
#
# def set_cpu_affinity(process, cpus):
#     p = psutil.Process(process.pid)
#     p.cpu_affinity(cpus)
#

if __name__ == "__main__":
    # vacancies bot (red, green) and flask endpoints
    p1 = Process(target=start_endpoints, args=())
    p2 = Process(target=start_bot, args=())
    p3 = Process(target=start_bot, args=(True, settings.token_red))

    # admin vacancies panel
    p4 = Process(target=start_admin_panel, args=())

    # simpleatom project
    p5 = Process(target=simpleatom_start, args=())
    p6 = Process(target=start_webForm_bot, args=())

    # auth django app
    p7 = Process(target=auth_start, args=())
    p75 = Process(target=start_individ_bot, args=())
    p76 = Process(target=start_flask_endpoints_indiv_bot, args=())

    # PARSERS
    # p77 = Process(target=start_parser_automatically, args=())
    # p78 = Process(target=start_other_parsers())
    # p79 = Process(target=start_hh_parser())

    # coffee project (horeca and customer bots with flask endpoints)
    # p8 = Process(target=start_customer_bot_FCM, args=())
    p9 = Process(target=start_horeca_bot_FCM, args=())
    # p10 = Process(target=start_endpoints_FCM, args=())
    # mock server
    # p11 = Process(target=mock_server_FCM, args=())

    # Not actual app
    # p12 = Process(target=talking_bot_run, args=())
    # p13 = Process(target=start_chat, args=())
    # p14 = Process(target=form_app_start, args=())

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p75.start()
    p76.start()
    # p77.start()
    # set_cpu_affinity(p77, [0])

    # p78.start()
    # p79.start()
    # set_cpu_affinity(p78, [0])
    # set_cpu_affinity(p79, [1])

    # p8.start()
    p9.start()
    # p10.start()
    # p11.start()
    # p12.start()
    # p13.start()
    # p14.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p75.join()
    p76.join()
    # p77.join()
    # p78.join()
    # p79.join()

    # p8.join()
    p9.join()
    # p10.join()
    # p11.join()
    # p12.join()
    # p13.join()
    # p14.join()
