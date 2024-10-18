from .storage import Storage
from .settings import settings
from .websites.ikman_scraper import IkmanScraper
from .websites.patpat_scraper import PatpatScraper
from .websites.riyasewana_scraper import RiyasewanaScraper
from scrapy.crawler import CrawlerProcess


process = None

def start_scraping():
    global process
    storage = Storage()
    process = CrawlerProcess(settings)

    process.crawl(IkmanScraper)
    process.crawl(PatpatScraper)
    process.crawl(RiyasewanaScraper)

    process.start()
    process.stop()
    print(storage.get_stats())
    # print(storage.get())


def stop_scraping():
    global process
    if process is not None:
        process.stop()
        print("Scraping stopped!")

    else:
        print("No scraping task to stop!")

