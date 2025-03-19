import asyncio
from threading import Thread
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from app.utils.logger import info, warn, err
from app.utils.message_queue import MessageQueue
from app.utils.storage import Storage
from app.db.repository.vehicle_repository import vehicles_repo
from .websites.ikman_scraper import IkmanScraper
from .websites.patpat_scraper import PatpatScraper
from .websites.riyasewana_scraper import RiyasewanaScraper

from .settings import settings


class Driver:
    """Class that manages the scraping process and the Twisted reactor."""

    def __init__(self):
        self.runner = CrawlerRunner(settings)
        self.reactor_thread = None
        self.is_scraping = False


    def start_scraping(self):
        """Start the scraping process."""
        if self.is_scraping:
            err("Scraping is already running.")
            return

        print("Starting the crawling process...")
        MessageQueue.set_enqueue_access(True)
        Storage.clear()
        vehicles_repo.drop()
        self.is_scraping = True

        # Start crawling the spiders
        d1 = self.runner.crawl(IkmanScraper)
        d2 = self.runner.crawl(PatpatScraper)
        d3 = self.runner.crawl(RiyasewanaScraper)

        defer.DeferredList([d1, d2, d3]).addCallback(self.on_all_spiders_finished)



    def on_all_spiders_finished(self, _):
        """Callback function that runs after all spiders have finished crawling."""
        self.is_scraping = False
        print(Storage.get_stats())
        print("Crawling process Finished...")
        vehicles_repo.save_all()



    async def stop_scraping(self):
        """Stop the scraping process gracefully."""
        if not self.is_scraping or not self.runner.crawlers:
            err("No scraping task to stop.")
            return

        for crawler in self.runner.crawlers:
            if crawler.crawling:
                print(f"Stopping {crawler.spider.name} spider...")
                crawler.engine.close_spider(crawler.spider, 'Stopped by user')

        MessageQueue.set_enqueue_access(False)

        # Wait for spiders to gracefully shut down
        while any(crawler.crawling for crawler in self.runner.crawlers):
            await asyncio.sleep(0.1)



    def start_reactor(self):
        """Start the Twisted reactor in a separate thread."""
        try:
            if not reactor.running:
                self.reactor_thread = Thread(target=reactor.run, args=(False,))
                self.reactor_thread.start()
                info("Twisted reactor started.")
        except Exception as e:
            err(f"Failed to start reactor: {e}")



    def stop_reactor(self):
        """Stop the Twisted reactor."""
        try:
            if reactor.running:
                reactor.stop()
                self.reactor_thread.join()
                self.reactor_thread = None
                info("Twisted reactor stopped.")
        except Exception as e:
            err(f"Failed to stop reactor: {e}")

driver = Driver()
