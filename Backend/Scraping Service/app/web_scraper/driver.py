# from .storage import Storage
# from .settings import settings
# from .websites.ikman_scraper import IkmanScraper
# from .websites.patpat_scraper import PatpatScraper
# from .websites.riyasewana_scraper import RiyasewanaScraper
# from scrapy.crawler import CrawlerProcess, CrawlerRunner

# import asyncio
# from concurrent.futures import ThreadPoolExecutor


# process = CrawlerProcess(settings)
# runner = CrawlerRunner(settings)

# # def start_scraping():
# #     global process
# #     storage = Storage()
# #     process = CrawlerProcess(settings)

# #     process.crawl(IkmanScraper)
# #     process.crawl(PatpatScraper)
# #     process.crawl(RiyasewanaScraper)

# #     process.start()
# #     print(storage.get_stats())
# #     # print(storage.get())


# async def start_scraping():
#     try:
#         global process
#         storage = Storage()
#         # process.crawl(IkmanScraper)
#         # process.crawl(PatpatScraper)
#         # process.crawl(RiyasewanaScraper)
#         # process.start()
#         await runner.crawl(RiyasewanaScraper)
#         print(storage.get_stats())
#         # print(storage.get())

#     except Exception as e:
#         print(f"An error occurred during scraping: {e}")


# def stop_scraping():
#     global process
#     if process is not None:
#         process.stop()
#         process = None
#         print("Scraping stopped!")

#     else:
#         print("No scraping task to stop!")






# async def start_scraping():
#     loop = asyncio.get_event_loop()
#     with ThreadPoolExecutor() as executor:
#         await loop.run_in_executor(executor, run_scraper)


from scrapy.crawler import CrawlerRunner
from scrapy import signals
from twisted.internet import reactor, defer
from threading import Thread

from .storage import Storage
from .settings import settings
from .websites.ikman_scraper import IkmanScraper
from .websites.patpat_scraper import PatpatScraper
from .websites.riyasewana_scraper import RiyasewanaScraper


runner = CrawlerRunner(settings)


def run_scraper():
    print("Starting the crawling process...")

    # Start crawling the spiders
    d1 = runner.crawl(IkmanScraper)
    d2 = runner.crawl(PatpatScraper)
    d3 = runner.crawl(RiyasewanaScraper)

    defer.DeferredList([d1, d2, d3]).addCallback(on_all_spiders_finished)


def on_all_spiders_finished(result):
    print("All spiders finished.")
    storage = Storage()
    print(storage.get_stats())


def stop_scraping():
    for crawler in runner.crawlers:
        if crawler.crawling:
            print(f"Stopping {crawler.spider.name}...")
            crawler.engine.close_spider(crawler.spider, 'Stopped by user')


def start_scraping():
    """Start the scraping process and the reactor."""
    stop_scraping()
    run_scraper()


def start_reactor():
    """Start the Twisted reactor in a separate thread."""
    thread = Thread(target=reactor.run, args=(False,))
    thread.start()


# Start the reactor when initializing FastAPI app
start_reactor()