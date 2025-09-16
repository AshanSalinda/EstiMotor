import asyncio
from twisted.internet.defer import DeferredList
from scrapy.crawler import CrawlerRunner
from app.data.site_data import ikman, patpat, riyasewana
from app.db.repository.ad_links_repository import ad_links_repo
from app.steps.shared.base_step import Step
from app.steps.step_1.websites.ikman_scraper import IkmanScraper
from app.steps.step_1.websites.patpat_scraper import PatpatScraper
from app.steps.step_1.websites.riyasewana_scraper import RiyasewanaScraper
from app.utils.logger import err
from app.utils.scrapy.progress_manager import ProgressManager
from app.utils.scrapy.settings import settings


class Driver(Step):
    """Class that manages the scraping process."""

    def __init__(self):
        super().__init__(step_name="Ads Collecting")
        self.runner = CrawlerRunner(settings)


    async def run(self):
        """Start the scraping process."""
        progress_manager = ProgressManager(target=0)

        try:
            ad_links_repo.drop()
            progress_manager.start_progress_emitter()

            # Start crawling the spiders
            d1 = self.runner.crawl(IkmanScraper, progress_manager=progress_manager, site_data=ikman)
            d2 = self.runner.crawl(PatpatScraper, progress_manager=progress_manager, site_data=patpat)
            d3 = self.runner.crawl(RiyasewanaScraper, progress_manager=progress_manager, site_data=riyasewana)

            await DeferredList([d1, d2, d3])

            progress_manager.stop_progress_emitter()
            progress_manager.complete()

        except Exception as e:
            progress_manager.stop_progress_emitter()
            raise e  # propagate to StepsManager


    async def stop_scraping(self):
        """Stop the scraping process gracefully."""
        if not self.is_running or not self.runner.crawlers:
            err("No scraping task to stop.")
            return

        for crawler in self.runner.crawlers:
            if crawler.crawling:
                print(f"Stopping {crawler.spider.name} spider...")
                crawler.engine.close_spider(crawler.spider, 'Stopped by user')

        # Wait for spiders to gracefully shut down
        while any(crawler.crawling for crawler in self.runner.crawlers):
            await asyncio.sleep(0.1)
