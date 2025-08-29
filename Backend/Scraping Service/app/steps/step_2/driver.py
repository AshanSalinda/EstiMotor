import asyncio
import json

from twisted.internet.defer import DeferredList
from scrapy.crawler import CrawlerRunner
from app.utils.logger import err
from app.utils.message_queue import MessageQueue
from app.utils.storage import Storage
from app.db.repository.ad_links_repository import ad_links_repo
from app.db.repository.scraped_vehicle_data_repository import scraped_vehicles_data_repo
from app.steps.shared.base_step import Step
from app.data.site_data import ikman, patpat, riyasewana
from .websites.ikman_scraper import IkmanScraper
from .websites.patpat_scraper import PatpatScraper
from .websites.riyasewana_scraper import RiyasewanaScraper
from .settings import settings


class Driver(Step):
    """Class that manages the scraping process."""

    def __init__(self):
        super().__init__(step_name="Details Extraction")
        self.runner = CrawlerRunner(settings)

    async def run(self):
        """Start the scraping process."""
        try:
            MessageQueue.set_enqueue_access(True)

            all_links = ad_links_repo.get_all()
            ikman_links = all_links.get(ikman['name'], [])
            patpat_links = all_links.get(patpat['name'], [])
            riyasewana_links = all_links.get(riyasewana['name'], [])
            all_links.clear()

            storage = Storage(data_type="list")

            # Start crawling the spiders
            d1 = self.runner.crawl(IkmanScraper, storage=storage, site_data=ikman, links=ikman_links)
            d2 = self.runner.crawl(PatpatScraper, storage=storage, site_data=patpat, links=patpat_links)
            d3 = self.runner.crawl(RiyasewanaScraper, storage=storage, site_data=riyasewana, links=riyasewana_links)

            await DeferredList([d1, d2, d3])
            print(json.dumps(storage.get_stats(), indent=2))
            scraped_vehicles_data_repo.drop()
            scraped_vehicles_data_repo.save(storage.get_data())
            # ad_links_repo.drop()
            storage.clear()

        except Exception as e:
            err(f"Error while running step 2: {e}")
            raise e

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
