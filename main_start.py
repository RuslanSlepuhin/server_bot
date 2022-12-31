import asyncio
import os
from threading import Thread, Event
import time
from _apps.endpoints import endpoints
from invite_bot_ver2 import run
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


def start_endpoints():
    # ev.wait()
    print('2')
    _apps.endpoints.endpoints.run_endpoints()

# lock = Lock()
#
if __name__ == "__main__":

    p1 = Process(target=start_endpoints, args=())
    p2 = Process(target=start_bot, args=())
    p1.start()
    p2.start()
    p1.join()
    p2.join()

