import asyncio
from twisted.internet.defer import DeferredList
from scrapy.crawler import CrawlerRunner
from app.utils.logger import err
from app.utils.message_queue import MessageQueue
from app.utils.storage import Storage
from app.db.repository.ad_links_repository import ad_links_repo
from app.steps.shared.base_step import Step
from app.data.site_data import ikman, patpat, riyasewana
from .websites.ikman_scraper import IkmanScraper
from .websites.patpat_scraper import PatpatScraper
from .websites.riyasewana_scraper import RiyasewanaScraper
from .settings import settings


class Driver(Step):
    """Class that manages the scraping process."""

    def __init__(self):
        super().__init__(step_name="Ads Collecting")
        self.runner = CrawlerRunner(settings)

    async def run(self):
        """Start the scraping process."""
        MessageQueue.set_enqueue_access(True)
        storage = Storage(data_type="dict")

        # Start crawling the spiders
        d1 = self.runner.crawl(IkmanScraper, storage=storage, site_data=ikman)
        d2 = self.runner.crawl(PatpatScraper, storage=storage, site_data=patpat)
        d3 = self.runner.crawl(RiyasewanaScraper, storage=storage, site_data=riyasewana)

        await DeferredList([d1, d2, d3])
        print(storage.get_stats())
        ad_links_repo.save(storage.get_data())
        storage.clear()

    async def stop_scraping(self):
        """Stop the scraping process gracefully."""
        if not self.is_running or not self.runner.crawlers:
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
