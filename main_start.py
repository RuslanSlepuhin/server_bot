import os
import time
from invite_bot_ver2 import run
from _apps.talking_bot.mvp_connect_talking_bot import talking_bot_run
from multiprocessing import Process
import settings.os_getenv as settings
# ev = Event()

num_processes = os.cpu_count()

def start_bot():
    time.sleep(10)
    # ev.wait()
    print('1')
    time.sleep(1)
    print('1-1')
    run()
    print('1-2')

def start_red_bot():
    time.sleep(10)
    # ev.wait()
    print('4')
    time.sleep(1)
    print('4-1')
    token_in = settings.token_red
    run(token_in)
    print('4-2')


def start_endpoints():
    # ev.wait()
    print('2')
    _apps.endpoints.endpoints.run_endpoints()

# lock = Lock()
#
if __name__ == "__main__":

    p1 = Process(target=start_endpoints, args=())
    p2 = Process(target=start_bot, args=())
    p3 = Process(target=talking_bot_run, args=())
    p4 = Process(target=start_red_bot, args=())

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    # p1.join()
    # p2.join()
    # p3.join()


