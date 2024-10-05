from utils.logger import info, warn, err
from scrapy.crawler import CrawlerProcess
from .web_scraper import WebScraper


class PatpatScraper(WebScraper):
    name = "patpat_scraper"

    def __init__(self, url, ad_link_selector, next_button_selector, *args, **kwargs):
        super(PatpatScraper, self).__init__(url, ad_link_selector, *args, **kwargs)


    def get_next_page(self, response):
        try:
            next_page = response.css('ul.pagination li:last-child a::attr(href)').get()
            return next_page if next_page else None
  
        except Exception as e:
            err(f"An error occurred during scraping: {e}")


    def get_vehicle_info(self, response):
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

        print(vehicle_details)
        # Print or log vehicle details


def run_scrapy():
    url = 'https://www.patpat.lk/vehicle?page=580'
    ad_link_selector = 'div.result-img a::attr(href)'
    next_button_selector = 'ul.pagination li:last-child a::attr(href)'

    process = CrawlerProcess(settings={
        "LOG_LEVEL": 'WARNING',
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
    })


    process.crawl(PatpatScraper, url, ad_link_selector, next_button_selector)
    process.start()

    warn("Scraping completed")


if __name__ == '__main__':
    run_scrapy()