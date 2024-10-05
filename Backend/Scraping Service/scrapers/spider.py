import scrapy
from scrapy.crawler import CrawlerProcess
from utils.logger import info, warn, err
from datetime import datetime



class VehicleSpider(scrapy.Spider):
    name = "patpat_scraper"
    start_urls = ['https://www.patpat.lk/vehicle?page=570']

    def __init__(self, *args, **kwargs):
        super(VehicleSpider, self).__init__(*args, **kwargs)
        self.page_count = 570
        self.startedAt = datetime.now()

    def parse(self, response):
        """Callback to parse a page and extract ad links."""
        info(f"Scraping page: {self.page_count}")
        self.page_count += 1

        # ad_links = response.css('div.result-img a::attr(href)').getall()
        # for link in ad_links:
        #     yield response.follow(link, callback=self.parse_vehicle_page)

        # Handle pagination
        # next_page = response.css('ul.pagination li:last-child a::attr(href)').get()
        # if next_page and 'disabled' not in response.css('ul.pagination li:last-child::attr(class)').get():
        #     yield response.follow(next_page, self.parse)

        next_page = response.css('ul.pagination li:last-child a::attr(href)').get()
        next_page_class = response.css('ul.pagination li:last-child::attr(class)').get()

        if next_page and (next_page_class is None or 'disabled' not in next_page_class):
            yield response.follow(next_page, self.parse)
        else:
            info(f"Scraping completed in {datetime.now() - self.startedAt}")


    def parse_vehicle_page(self, response):
        """Callback to extract vehicle details from a specific ad page."""
        vehicle_details = {}

        title = response.css('h2.item-title::text').get()
        price = response.css('p.m-0.col-6.col-sm-7.p-0.m-0 span::text').getall()
        table_rows = response.css('table.course-info tr')

        if title:
            vehicle_details['title'] = title.strip()

        if len(price) == 2:
            vehicle_details['price'] = price[1].strip()

        for row in table_rows:
            key = row.css('td.w-25::text').get()
            value = row.css('td.w-75::text').get()
            if key and value:
                vehicle_details[key.strip().replace(':', '')] = value.strip()

        # Print or log vehicle details
        info(f"Scraped Vehicle: {vehicle_details}")
        yield vehicle_details  # This sends the scraped data to the output

# To run this spider, use the Scrapy CLI: `scrapy runspider patpat_scraper.py`




# Programmatically running the spider
def run_scrapy():
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "WARNING", # You can set the logging level here
    })

    # Start the crawling using the VehicleSpider
    process.crawl(VehicleSpider)
    process.start()  # This blocks the script until crawling is finished

if __name__ == '__main__':
    run_scrapy()
