import threading
import time
from asyncio import run
from sites.scraping_hh import HHGetInformation
from report.reports import Reports


"""
[junior, backend, frontend, qa, devops, designer, game, mobile, product, pm, analyst, marketing, sales_manager, hr]
"""
report = Reports


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


def run_hh_sales():
    sales_scraper = HHGetInformation(report=report)
    run(sales_scraper.get_content(words_pattern=['sales manager']))

def run_hh_hr():
    hr_scraper = HHGetInformation(report=report)
    run(hr_scraper.get_content(words_pattern=['hr']))


def run_hh_threadings():
    thread_junior = threading.Thread(target=run_hh_junior)
    thread_backend = threading.Thread(target=run_hh_backend)
    thread_frontend = threading.Thread(target=run_hh_frontend)
    thread_qa = threading.Thread(target=run_hh_qa)
    thread_devops = threading.Thread(target=run_hh_devops)
    thread_designer = threading.Thread(target=run_hh_designer)
    thread_game = threading.Thread(target=run_hh_game)
    thread_mobile = threading.Thread(target=run_hh_mobile)
    thread_product = threading.Thread(target=run_hh_product)
    thread_pm = threading.Thread(target=run_hh_pm)
    thread_analyst = threading.Thread(target=run_hh_analyst)
    thread_marketing = threading.Thread(target=run_hh_marketing)
    thread_sales = threading.Thread(target=run_hh_sales)
    thread_hr = threading.Thread(target=run_hh_hr)

    thread_junior.start()
    time.sleep(3)
    thread_backend.start()
    time.sleep(3)
    thread_frontend.start()
    time.sleep(3)
    thread_qa.start()
    time.sleep(3)
    thread_devops.start()
    time.sleep(3)
    thread_designer.start()
    time.sleep(3)
    thread_game.start()
    time.sleep(3)
    thread_mobile.start()
    time.sleep(3)
    thread_product.start()
    time.sleep(3)
    thread_pm.start()
    time.sleep(3)
    thread_analyst.start()
    time.sleep(3)
    thread_marketing.start()
    time.sleep(3)
    thread_sales.start()
    time.sleep(3)
    thread_hr.start()

    thread_junior.join()
    thread_backend.join()
    thread_frontend.join()
    thread_qa.join()
    thread_devops.join()
    thread_designer.join()
    thread_game.join()
    thread_mobile.join()
    thread_product.join()
    thread_pm.join()
    thread_analyst.join()
    thread_marketing.join()
    thread_sales.join()
    thread_hr.join()


if __name__ == "__main__":
    run_hh_threadings()
