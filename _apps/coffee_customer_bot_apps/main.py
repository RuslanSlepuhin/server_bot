import configparser
from _apps.coffee_customer_bot_apps.back_server_side.back_server_side import BackServer
from _apps.coffee_customer_bot_apps.coffee_customer_bot.coffee_customer_bot import CustomerBot
from _apps.coffee_customer_bot_apps.coffee_horeca_bot.coffee_horeca_bot import HorecaBot
from multiprocessing import Process
from _apps.coffee_customer_bot_apps.endpoints.endpoints import Endpoints


config = configparser.ConfigParser()
config.read('./_apps/coffee_customer_bot_apps/settings/config.ini')

customer_token = config['Bot']['customer_token']
horeca_token = config['Bot']['horeca_token']
horeca_bot = HorecaBot()
customer_bot = CustomerBot()


def start_customer_bot():
    customer_bot.bot_handlers()

def start_horeca_bot():
    horeca_bot.bot_handlers()

def start_endpoints():
    ep = Endpoints()
    ep.main_endpoints(customer_bot, horeca_bot)

def start_back_server():
    back_server = BackServer()
    back_server.main_back_server()

def start_method():
    p1 = Process(target=start_customer_bot, args=())
    p2 = Process(target=start_horeca_bot, args=())
    p3 = Process(target=start_endpoints, args=())
    p4 = Process(target=start_back_server, args=())

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

if __name__ == '__main__':
    start_method()