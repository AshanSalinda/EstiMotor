import scrapy
from utils.logger import info, warn, err
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs


class WebScraper(scrapy.Spider):
    def __init__(self, url, ad_selector, *args, **kwargs):
        super(WebScraper, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.ad_selector = ad_selector


    def start_requests(self):
        """This is called when the spider starts crawling"""

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.scrape, errback=self.on_error)


    def closed(self, reason):
        """This is called when the spider finishes crawling"""

        start_time = self.crawler.stats.get_value('start_time')
        finish_time = datetime.now(timezone.utc)
        time_taken = str(finish_time - start_time)
        time = time_taken.split('.')[0]
        ms = int(time_taken.split('.')[1]) // 1000

        stats = {
            'error_responses': self.crawler.stats.get_value('downloader/response_status_count/500', 0),
            'success_requests': self.crawler.stats.get_value('downloader/response_status_count/200', 0),
            'not_found_responses': self.crawler.stats.get_value('downloader/response_status_count/404', 0),
            'failed_with_timeout': self.crawler.stats.get_value('downloader/exception_type_count/twisted.internet.error.TimeoutError', 0),
            'failed_with_network_error': self.crawler.stats.get_value('downloader/exception_type_count/twisted.internet.error.DNSLookupError', 0),
            'time_taken': f"{time}.{ms}"
        }

        info(stats)

    
    def on_error(self, failure):
        """This is called when an error occurs during a request"""

        url = failure.request.url
        index = failure.request.meta.get('index', '0:0')
        err(f"{index}\t{url}")


    def scrape(self, response):
        """This is the default callback for every request for pages, made by the spider"""
        try:
            # Extract the 'page' parameter value from the url
            page_no = parse_qs(urlparse(response.url).query).get('page', [1])[0] 
            info(f"Scraping page: {page_no}")

            # Extract All Ads links and get ad details
            ad_links = response.css(f"{self.ad_selector}::attr(href)").getall()
            for index, link in enumerate(ad_links):
                yield response.follow(
                    link, 
                    callback=self.get_vehicle_info, 
                    errback=self.on_error, 
                    meta={'index': f"{page_no}:{index + 1}"}
                )

            # Handle pagination
            next_page = self.get_next_page(response)
            if next_page:
                yield response.follow(next_page, callback=self.scrape, errback=self.on_error)
        
        except Exception as e:
            err(f"An error occurred during scraping: {e}")



    def get_vehicle_info(self, response):
        err(f"{self.name} must implement a own get_vehicle_info method")


    def get_next_page(self, response):
        err(f"{self.name} must implement a own get_next_page method")


