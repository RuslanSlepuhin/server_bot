import asyncio
import threading
from utils.additional_variables.additional_variables import valid_professions

from report.reports import Reports
from sites._scraping_remotejob import RemoteJobGetInformation
from sites.scraping_careerjet import СareerjetGetInformation
from sites.scraping_dev import DevGetInformation
from sites.scraping_epam_anywhere import EpamGetInformation
from sites.scraping_habr import HabrGetInformation
from sites.scraping_hh import HHGetInformation
from sites.scraping_hh_it import HHITGetInformation
from sites.scraping_hhkz import HHKzGetInformation
from sites.scraping_geekjob import GeekGetInformation
from sites.scraping_otta import OttaGetInformation
from sites.scraping_praca import PracaGetInformation
from sites.scraping_remocate import RemocateGetInformation
from sites.scraping_wellfound import WellFoundGetInformation
from sites.scrapping_finder import FinderGetInformation

report = Reports()


def run_hh():
    hh = HHGetInformation(report=report)
    asyncio.run(hh.get_content(words_pattern=valid_professions))


async def run_others():
    # await HHKzGetInformation(report=report).get_content(words_pattern=valid_professions)
    await GeekGetInformation(report=report).get_content()
    await EpamGetInformation(report=report).get_content(words_pattern=valid_professions)
    await DevGetInformation(report=report).get_content(words_pattern=valid_professions)
    await СareerjetGetInformation(report=report).get_content(words_pattern=valid_professions)
    await HabrGetInformation(report=report).get_content()
    await FinderGetInformation(report=report).get_content(words_pattern=valid_professions)
    await PracaGetInformation(report=report).get_content(words_pattern=valid_professions)
    await RemocateGetInformation(report=report).get_content()
    await HHITGetInformation(report=report).get_content(words_pattern=valid_professions)
    await RemoteJobGetInformation(report=report).get_content()
    await OttaGetInformation(report=report).get_content()
    await WellFoundGetInformation(report=report).get_content()


def run_asyncio_tasks():
    asyncio.run(run_others())


def common_run_parsers():
    thread_hh = threading.Thread(target=run_hh)
    thread_other = threading.Thread(target=run_asyncio_tasks)

    thread_hh.start()
    thread_other.start()

    thread_hh.join()
    thread_other.join()


if __name__ == "__main__":
    common_run_parsers()
