import scrapy
from utils.logger import info, warn, err
from ..Items.Items import VehicleItem
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs, urlencode


class WebScraper(scrapy.Spider):
    """Base class for website-specific scrapers"""
    def __init__(self, url, ad_selector, *args, **kwargs):
        super(WebScraper, self).__init__(*args, **kwargs)
        self.VehicleItem = VehicleItem
        self.start_urls = [url]
        self.ad_selector = ad_selector


    def start_requests(self):
        """Called when the spider starts crawling"""
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.scrape, errback=self.on_error)


    def closed(self, reason):
        """Called when the spider finishes crawling"""

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
        """Handle request errors"""
        url = failure.request.url
        index = failure.request.meta.get('index', '0:0')
        err(f"{index}\t{url}")
        print(failure)


    def scrape(self, response):
        """This is the default callback for every request for pages, made by the spider"""
        try:
            current_url = response.url
            query_params = parse_qs(urlparse(current_url).query)
            page_no = int(query_params.get('page', [1])[0] )
            info(f"Scraping page: {page_no}")

            # Extract All Ads links
            ad_links = response.css(f"{self.ad_selector}::attr(href)").getall()

            # Get the vehicle info for each ad
            for index, link in enumerate(ad_links):
                if self.name == "ikman_scraper":
                    link = f"https://ikman.lk{link}"

                yield response.follow(
                    link, 
                    callback=self.get_vehicle_info, 
                    errback=self.on_error, 
                    meta={'index': f"{page_no}:{index + 1}"}
                )

            # Handle pagination
            last_page = self.is_last_page(response)
            if not last_page:
                query_params['page'] = page_no + 1
                new_query = urlencode(query_params)
                next_page_url = f"{current_url.split('?')[0]}?{new_query}"

                yield response.follow(next_page_url, callback=self.scrape, errback=self.on_error)
        
        except Exception as e:
            err(f"An error occurred during scraping: {e}")



    def get_vehicle_info(self, response):
        err(f"{self.name} must implement a own get_vehicle_info method")


    def is_last_page(self, response):
        err(f"{self.name} must implement a own is_last_page method")


