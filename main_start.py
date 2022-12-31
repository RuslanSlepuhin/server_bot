import asyncio
import os
from threading import Thread, Event
import time
import endpoints.endpoints
from invite_bot_ver2 import run
from _apps.talking_bot.mvp_connect_talking_bot import talking_bot_run
from multiprocessing import Process, Lock
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

def start_talking_bot_run():
    time.sleep(5)
    print('3')
    time.sleep(1)
    print('3-1')
    talking_bot_run()
    print('3-2')


def start_endpoints():
    # ev.wait()
    print('2')
    endpoints.endpoints.run_endpoints()



# lock = Lock()
#
if __name__ == "__main__":

    p1 = Process(target=start_endpoints, args=())
    p2 = Process(target=start_bot, args=())
    p3 = Process(target=start_talking_bot_run, args=())

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()


