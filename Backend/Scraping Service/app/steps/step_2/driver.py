import asyncio

from twisted.internet.defer import DeferredList, ensureDeferred
from scrapy.crawler import CrawlerRunner
from app.config import settings
from app.utils.logger import err, info
from app.utils.message_queue import MessageQueue
from app.db.repository.ad_links_repository import ad_links_repo
from app.db.repository.scraped_vehicle_data_repository import scraped_vehicles_data_repo
from app.steps.shared.base_step import Step
from app.data.site_data import ikman, patpat, riyasewana
from .websites.ikman_scraper import IkmanScraper
from .websites.patpat_scraper import PatpatScraper
from .websites.riyasewana_scraper import RiyasewanaScraper
from .settings import settings as crawler_settings
from ...utils.ProgressManager import ProgressManager


class Driver(Step):
    """Class that manages the scraping process."""

    def __init__(self):
        super().__init__(step_name="Details Extraction")
        self.runner = CrawlerRunner(crawler_settings)
        self.progress_manager = None
        self.batch_size = settings.SCRAPING_BATCH_SIZE
        self.websites = [
            {"data": ikman, "scraper": IkmanScraper},
            {"data": patpat, "scraper": PatpatScraper},
            {"data": riyasewana, "scraper": RiyasewanaScraper},
        ]

    async def run(self):
        """Run all websites iteratively in batch mode."""
        try:
            scraped_vehicles_data_repo.drop()
            MessageQueue.set_enqueue_access(True)
            total_links = ad_links_repo.get_total_ad_count()
            self.progress_manager = ProgressManager(target=total_links)
            self.progress_manager.start_scheduled_job()

            # Create Twisted Deferreds
            deferreds = [ensureDeferred(self.run_site_batch(site_info)) for site_info in self.websites]

            # Wait for all sites in parallel
            await DeferredList(deferreds, fireOnOneErrback=True)

            self.progress_manager.end()
            # ad_links_repo.drop()

        except Exception as e:
            err(f"Error while running step 2: {e}")
            raise e

    async def run_site_batch(self, site_info: dict):
        """Scrape a single website batch-wise."""

        name = site_info["data"]["name"]
        scraper = site_info["scraper"]
        processed_so_far = 0

        while True:
            # Get first batch
            batch_links = ad_links_repo.get_by_source_in_paginated(name, page_size=self.batch_size)
            if not batch_links:
                info(f"No more links for {name}.")
                break

            link_urls = []
            link_ids = []
            scraped_data = []

            for doc in batch_links:
                link_ids.append(doc.get("_id"))
                link_urls.append(doc.get("url"))

            info(f"Processing {len(link_urls)} links for {name}...")
            d = self.runner.crawl(
                scraper,
                site_data=site_info["data"],
                progress_manager=self.progress_manager,
                scraped_data=scraped_data,
                links=link_urls,
                processed_so_far=processed_so_far
            )

            await DeferredList([d])

            # Save scraped data and remove processed links
            scraped_vehicles_data_repo.save(scraped_data)
            scraped_data.clear()
            ad_links_repo.delete_by_ids(link_ids)
            processed_so_far += len(link_urls)

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
