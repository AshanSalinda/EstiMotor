from .storage import Storage
from .settings import settings
from .websites.ikman_scraper import IkmanScraper
from .websites.patpat_scraper import PatpatScraper
from .websites.riyasewana_scraper import RiyasewanaScraper
from scrapy.crawler import CrawlerProcess


def run_scrapy():
    storage = Storage()
    process = CrawlerProcess(settings)

    process.crawl(IkmanScraper)
    process.crawl(PatpatScraper)
    process.crawl(RiyasewanaScraper)

    process.start()
    process.stop()
    print(storage.get_stats())
    # print(storage.get())

