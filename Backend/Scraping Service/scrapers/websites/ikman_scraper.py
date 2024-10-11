from utils.logger import info, warn, err
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from ..spyder.web_scraper import WebScraper


class PatpatScraper(WebScraper):
    name = "ikman_scraper"

    def __init__(self, url, selectors, *args, **kwargs):
        self.pagination = selectors['pagination']
        self.title = selectors['title']
        self.price = selectors['price']
        self.table = selectors['table']
        ad_selector = selectors['ads_link']
        super(PatpatScraper, self).__init__(url, ad_selector, *args, **kwargs)


    def is_last_page(self, response):
        try:
            # Extract the pagination element
            pagination = response.css(self.pagination).get()
            return pagination == None
  
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")


    def get_vehicle_info(self, response):
        try:
            vehicle_item = self.VehicleItem()
            vehicle_details = {}
            title = response.css(f"{self.title}::text").get()
            price = response.css(f"{self.price}::text").get()
            table = response.css(self.table)

            if price:
                vehicle_item['price'] = price.strip('Rs ').replace(',', '')
            else:
                raise Exception("Price not found")


            if title:
                vehicle_item['title'] = title.strip()
            else:
                raise Exception("Title not found")
                

            for row in table:
                key = row.css('div:nth-child(1)::text').get()
                value_el = row.css('div:nth-child(2)')
                value = value_el.css('div a span::text').get() or value_el.css('::text').get()

                if key and value and type(key) == str and type(value) == str:
                    vehicle_details[key.strip().replace(':', '')] = value.strip()

            vehicle_item['details'] = vehicle_details
            vehicle_item['url'] = response.url
            yield vehicle_item

            print(f"{response.meta.get('index')}\t{response.url}")

        except Exception as e:
            err(f"{response.meta.get('index')}\t{response.url}\n{e}")


def run_scrapy():
    url = 'https://ikman.lk/en/ads/sri-lanka/cars?page=137'
    selectors = {
        'ads_link': 'ul.list--3NxGO li a',
        'pagination': 'div.pagination--1bp3g nav',
        'title': 'h1.title--3s1R8',
        'price': 'div.amount--3NTpl',
        'table': 'div.ad-meta--17Bqm div.full-width--XovDn',
    }


    process = CrawlerProcess(settings={
        "LOG_LEVEL": 'WARNING',
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
        "BOT_NAME": 'EstiMotor_scraper',
        "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    })


    process.crawl(PatpatScraper, url, selectors)
    process.start()


if __name__ == '__main__':
    run_scrapy()