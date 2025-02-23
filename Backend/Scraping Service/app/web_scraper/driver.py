import asyncio
from threading import Thread
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from app.utils.logger import info, warn, err
from app.utils.message_queue import MessageQueue
from app.db.repository.vehicle_repository import vehicles_repo
from .websites.ikman_scraper import IkmanScraper
from .websites.patpat_scraper import PatpatScraper
from .websites.riyasewana_scraper import RiyasewanaScraper
from .storage import Storage
from .settings import settings


runner = CrawlerRunner(settings)
reactor_thread = None
is_scraping = False


def start_scraping():
    global is_scraping

    if is_scraping:
        err("Scraping is already running.")
        return

    print("Starting the crawling process...")
    MessageQueue.set_enqueue_access(True)
    Storage.clear()
    vehicles_repo.drop()
    is_scraping = True

    # Start crawling the spiders
    d1 = runner.crawl(IkmanScraper)
    d2 = runner.crawl(PatpatScraper)
    d3 = runner.crawl(RiyasewanaScraper)

    defer.DeferredList([d1, d2, d3]).addCallback(on_all_spiders_finished)


def on_all_spiders_finished(_):
    global is_scraping
    
    is_scraping = False
    print(Storage.get_stats())
    print("Crawling process Finished...")
    vehicles_repo.save_all()


async def stop_scraping():
    global is_scraping
    if not is_scraping or not runner.crawlers:
        err("No scraping task to stop.")
        return

    for crawler in runner.crawlers:
        if crawler.crawling:
            print(f"Stopping {crawler.spider.name} spider...")
            crawler.engine.close_spider(crawler.spider, 'Stopped by user')
    
    MessageQueue.set_enqueue_access(False)
    
    # Wait for spiders to gracefully shut down
    while any(crawler.crawling for crawler in runner.crawlers):
        await asyncio.sleep(0.1)


def start_reactor():
    """Start the Twisted reactor in a separate thread."""
    global reactor_thread
    
    try:
        if not reactor.running:
            reactor_thread = Thread(target=reactor.run, args=(False,))
            reactor_thread.start()
            info("Twisted reactor started.")
    except Exception as e:
        err(f"Failed to start reactor: {e}")
    


def stop_reactor():
    """Stop the Twisted reactor."""
    global reactor_thread

    try:
        if reactor.running:
            reactor.stop()
            reactor_thread.join()
            reactor_thread = None
            info("Twisted reactor stopped.")
    except Exception as e:
        err(f"Failed to stop reactor: {e}")