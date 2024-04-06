import configparser

import utils.additional_variables.additional_variables
from db_operations.scraping_db import DataBaseOperations
from logs.logs import Logs
from sites.scraping_careerjet import СareerjetGetInformation
from sites._scraping_careerspace import CareerSpaceGetInformation
from sites.scraping_designer import DesignerGetInformation
from sites.scraping_dev import DevGetInformation
from sites.scraping_epam_anywhere import EpamGetInformation
from sites.scraping_geekjob import GeekGetInformation
from sites.scraping_habr import HabrGetInformation
from sites.scraping_hh import HHGetInformation
from sites.scraping_hhkz import HHKzGetInformation
from sites.scraping_praca import PracaGetInformation
from sites.scraping_rabota import RabotaGetInformation
from sites.scraping_remocate import RemocateGetInformation
from sites.scraping_remotehub import RemotehubGetInformation
from sites._scraping_remotejob import RemoteJobGetInformation
from sites._scraping_superjob import SuperJobGetInformation
from sites.scraping_svyazi import SvyaziGetInformation
from sites.scraping_gorodrabot import GorodRabotGetInformation
from sites.scrapping_finder import FinderGetInformation
from sites.scraping_ingamejob import IngameJobGetInformation
from sites._scraping_remotejob_upgrade import RemoteJobGetInformation
from sites.scraping_otta import OttaGetInformation
from helper_functions import helper_functions as helper

logs = Logs()

config = configparser.ConfigParser()
config.read("./settings_/config.ini")

parser_sites = {'nn.hh.ru': HHGetInformation, 'spb.hh.ru': HHGetInformation, 'hh.ru': HHGetInformation,
                'hh.kz': HHKzGetInformation, 'rabota.by': RabotaGetInformation, 'praca.by': PracaGetInformation,
                'remotehub.com': RemotehubGetInformation, 'remote-job.ru': RemoteJobGetInformation,
                'jobs.devby.io' : DevGetInformation, 'russia.superjob.ru': SuperJobGetInformation,
                'superjob.ru': SuperJobGetInformation, 'career.habr.com': HabrGetInformation,
                'u.habr.com': HabrGetInformation,'finder.vc': FinderGetInformation, 'geekjob.ru' : GeekGetInformation,
                'gkjb.ru': GeekGetInformation, 'designer.ru': DesignerGetInformation,
                'www.vseti.app': SvyaziGetInformation, 'ru.ingamejob.com': IngameJobGetInformation, 'rabota.by': GorodRabotGetInformation}


class SitesParser:

    def __init__(self, client, bot_dict, **kwargs):
        self.report = kwargs['report'] if 'report' in kwargs else None
        self.client = client
        self.current_session = ''
        self.bot = bot_dict['bot']
        self.chat_id = bot_dict['chat_id']
        self.db = DataBaseOperations(report=self.report)
        self.helper = helper



    async def call_sites(self):

        bot_dict = {'bot': self.bot, 'chat_id': self.chat_id}

        await HHGetInformation(main_class=self, bot_dict=bot_dict, report=self.report).get_content(words_pattern=utils.additional_variables.additional_variables.valid_professions)
        await HHKzGetInformation(main_class=self, bot_dict=bot_dict, report=self.report).get_content(words_pattern=utils.additional_variables.additional_variables.valid_professions)
        await GeekGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await EpamGetInformation(main_class=self, bot_dict=bot_dict, report=self.report).get_content(words_pattern=utils.additional_variables.additional_variables.valid_professions)
        await DevGetInformation(main_class=self, bot_dict=bot_dict, report=self.report).get_content(words_pattern=utils.additional_variables.additional_variables.valid_professions)
        await СareerjetGetInformation(main_class=self, bot_dict=bot_dict, report=self.report).get_content(words_pattern=utils.additional_variables.additional_variables.valid_professions)
        await FinderGetInformation(main_class=self, bot_dict=bot_dict, report=self.report).get_content(words_pattern=utils.additional_variables.additional_variables.valid_professions)

        await GorodRabotGetInformation(bot_dict=bot_dict, db=self.db, helper=self.helper).get_content()
        await CareerSpaceGetInformation(bot_dict=bot_dict, report=self.report, db=self.db,
                                        helper=self.helper).get_content()
        await DesignerGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        # await FindJobGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await IngameJobGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await RabotaGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await PracaGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await HabrGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await DesignerGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await RemotehubGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await RemoteJobGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await SuperJobGetInformation(bot_dict=bot_dict, report=self.report).get_content()
        await SvyaziGetInformation(bot_dict=bot_dict, report=self.report).get_content()

        await OttaGetInformation(bot_dict=bot_dict, report=self.report).get_content()

        print(' -----------------------FINAL -------------------------------')

