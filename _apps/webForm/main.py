import asyncio
import os
from multiprocessing import Process
from telegram.bot_webhooks import WebhookBot
num_processes = os.cpu_count()

def start_bot():
    token = '6928876462:AAEaBttMIEhZhi4Hh7U1GKDVFL2693wNpvY'
    bot = WebhookBot()
    bot.main()

def start_web():
    import os
    from django.core.management import execute_from_command_line

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webForm.settings')
    execute_from_command_line(['manage.py', 'runserver'])



if __name__ == "__main__":

    p1 = Process(target=start_bot, args=())
    p2 = Process(target=start_web, args=())

    p1.start()
    p2.start()

    p1.join()
    p2.join()


