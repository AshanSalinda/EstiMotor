import scrapy
from utils.logger import info, warn, err
from datetime import datetime, timezone


class WebScraper(scrapy.Spider):
    def __init__(self, url, ad_link_selector, *args, **kwargs):
        super(WebScraper, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.ad_link_selector = ad_link_selector
        self.started_at = datetime.now()
        self.all_vehicle_data = []
        self.page_count = 0


    def closed(self, reason):
        """This is called when the spider finishes crawling"""

        start_time = self.crawler.stats.get_value('start_time')
        finish_time = datetime.now(timezone.utc)
        time_taken = str(finish_time - start_time)
        time = time_taken.split('.')[0]
        ms = int(time_taken.split('.')[1]) // 1000

        success_requests = self.crawler.stats.get_value('downloader/response_status_count/200', 0)
        failed_requests = self.crawler.stats.get_value('downloader/response_status_count/500', 0)
        not_found_requests = self.crawler.stats.get_value('downloader/response_status_count/404', 0)
        failed_request_other = self.crawler.stats.get_value('downloader/exception_type_count/twisted.internet.error.TimeoutError', 0) 
        failed_request_network = self.crawler.stats.get_value('downloader/exception_type_count/twisted.internet.error.DNSLookupError', 0) 
        print(f"Failed requests: {failed_requests}")
        print(f"Successful requests: {success_requests}")
        print(f"Not found requests: {not_found_requests}")
        print(f"Other failed requests: {start_time}")
        print(f"network errors {finish_time}")
        print(f"Scraping completed in: {time}.{ms}")


    def parse(self, response):
        """This is the default callback for every request made by the spider"""

        try:       
            info(f"Scraping page: {self.page_count}")

            ad_links = response.css('div.result-img a::attr(href)').getall()
            for link in ad_links:
                yield response.follow(link, callback=self.get_vehicle_info)

            # Handle pagination
            next_page = self.get_next_page(response)
            if next_page:
                yield response.follow(next_page, callback=self.parse)

            self.page_count += 1
        
        except Exception as e:
            err(f"An error occurred during scraping: {e}")



    def get_vehicle_info(self, response):
        err(f"{self.name} must implement a own get_vehicle_info method")


    def get_next_page(self, response):
        err(f"{self.name} must implement a own get_next_page method")


