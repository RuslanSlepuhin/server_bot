
import configparser
from logs.logs import Logs
from sites.scraping_geekjob import GeekGetInformation
from sites.scraping_habr import HabrGetInformation
from sites.scraping_hh import HHGetInformation
from sites.scraping_rabota import RabotaGetInformation
from sites.scraping_svyazi import SvyaziGetInformation
from sites.scrapping_finder import FinderGetInformation

logs = Logs()

config = configparser.ConfigParser()
config.read("./settings_/config.ini")

class ParseSites:

    def __init__(self, client, bot_dict):
        self.client = client
        self.current_session = ''
        self.bot = bot_dict['bot']
        self.chat_id = bot_dict['chat_id']


    async def call_sites(self):

        logs.write_log(f"scraping_telethon2: function: call_sites")

        bot_dict = {'bot': self.bot, 'chat_id': self.chat_id}
        await HHGetInformation(bot_dict).get_content()
        await RabotaGetInformation(bot_dict).get_content()
        await HabrGetInformation(bot_dict).get_content()
        await FinderGetInformation(bot_dict).get_content()
        await GeekGetInformation(bot_dict).get_content()
        await SvyaziGetInformation(bot_dict).get_content()

        print(' -----------------------FINAL -------------------------------')

