import threading
import time
from asyncio import run
from sites.scraping_hh import HHGetInformation
from report.reports import Reports


report = Reports()


def run_hh_junior():
    junior_scraper = HHGetInformation(report=report)
    run(junior_scraper.get_content(words_pattern=['junior']))


def run_hh_backend():
    backend_scraper = HHGetInformation(report=report)
    run(backend_scraper.get_content(words_pattern=['backend']))


def run_hh_frontend():
    frontend_scraper = HHGetInformation(report=report)
    run(frontend_scraper.get_content(words_pattern=['frontend']))


def run_hh_qa():
    qa_scraper = HHGetInformation(report=report)
    run(qa_scraper.get_content(words_pattern=['qa']))


def run_hh_devops():
    devops_scraper = HHGetInformation(report=report)
    run(devops_scraper.get_content(words_pattern=['devops']))


def run_hh_designer():
    designer_scraper = HHGetInformation(report=report)
    run(designer_scraper.get_content(words_pattern=['designer']))


def run_hh_game():
    game_scraper = HHGetInformation(report=report)
    run(game_scraper.get_content(words_pattern=['game']))


def run_hh_mobile():
    mobile_scraper = HHGetInformation(report=report)
    run(mobile_scraper.get_content(words_pattern=['mobile']))


def run_hh_product():
    product_scraper = HHGetInformation(report=report)
    run(product_scraper.get_content(words_pattern=['product']))


def run_hh_pm():
    pm_scraper = HHGetInformation(report=report)
    run(pm_scraper.get_content(words_pattern=['pm']))


def run_hh_analyst():
    analyst_scraper = HHGetInformation(report=report)
    run(analyst_scraper.get_content(words_pattern=['analyst']))


def run_hh_marketing():
    marketing_scraper = HHGetInformation(report=report)
    run(marketing_scraper.get_content(words_pattern=['marketing']))


def run_hh_sales_manager():
    sales_scraper = HHGetInformation(report=report)
    run(sales_scraper.get_content(words_pattern=['sales manager']))

def run_hh_hr():
    hr_scraper = HHGetInformation(report=report)
    run(hr_scraper.get_content(words_pattern=['hr']))


def run_hh_threadings():
    items = [
        'junior',
        'backend',
        'frontend',
        'qa',
        'devops',
        'designer',
        'game',
        'mobile',
        'product',
        'pm',
        'analyst',
        'marketing',
        'sales_manager',
        'hr'
    ]

    for item in items:
        exec(f"thread_{item} = threading.Thread(target=run_hh_{item})")

    for item in items:
        exec(f"thread_{item}.start()")
        time.sleep(3)

    for item in items:
        exec(f"thread_{item}.join()")


if __name__ == "__main__":
    run_hh_threadings()
