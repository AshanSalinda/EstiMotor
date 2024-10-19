from threading import Thread
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from ..utils.logger import info, warn, err
from .storage import Storage
from .settings import settings
from .websites.ikman_scraper import IkmanScraper
from .websites.patpat_scraper import PatpatScraper
from .websites.riyasewana_scraper import RiyasewanaScraper


runner = CrawlerRunner(settings)
reactor_thread = None
is_scraping = False


def start_scraping():
    global is_scraping

    if is_scraping:
        err("Scraping is already running.")
        return

    print("Starting the crawling process...")
    is_scraping = True

    # Start crawling the spiders
    d1 = runner.crawl(IkmanScraper)
    d2 = runner.crawl(PatpatScraper)
    d3 = runner.crawl(RiyasewanaScraper)

    defer.DeferredList([d1, d2, d3]).addCallback(on_all_spiders_finished)


def on_all_spiders_finished(result):
    global is_scraping
    print("All spiders finished.")
    is_scraping = False
    storage = Storage()
    print(storage.get_stats())


def stop_scraping():
    global is_scraping
    if not is_scraping or not runner.crawlers:
        err("No scraping task to stop.")
        return

    for crawler in runner.crawlers:
        if crawler.crawling:
            print(f"Stopping {crawler.spider.name}...")
            crawler.engine.close_spider(crawler.spider, 'Stopped by user')

    is_scraping = False


def start_reactor():
    """Start the Twisted reactor in a separate thread."""
    global reactor_thread
    if not reactor.running:
        reactor_thread = Thread(target=reactor.run, args=(False,))
        reactor_thread.start()
        info("\t  Twisted reactor started.")


def stop_reactor():
    """Stop the Twisted reactor."""
    global reactor_thread
    if reactor.running:
        reactor.stop()
        reactor_thread.join()
        reactor_thread = None
        info("\t  Twisted reactor stopped.")