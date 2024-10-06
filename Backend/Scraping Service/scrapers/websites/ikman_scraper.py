from utils.logger import info, warn, err
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from playwright.async_api import async_playwright
from ..spyder.web_scraper import WebScraper


class PatpatScraper(WebScraper):
    name = "ikman_scraper"

    def __init__(self, url, selectors, *args, **kwargs):
        self.next_button = selectors['next_button']
        self.title = selectors['title']
        self.price = selectors['price']
        self.rows = selectors['rows']
        self.key = selectors['key']
        self.value = selectors['value']
        ad_selector = selectors['ads_link']
        super(PatpatScraper, self).__init__(url, ad_selector, *args, **kwargs)


    async def is_last_page(self, response):
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(response.url, wait_until='domcontentloaded')
                html = await page.content()
                res = Selector(text=html)
                await browser.close()

                # Extract the pagination element
                pagination = res.css('div.pagination--1bp3g').get()
                print(pagination)

                disabled_next_button = response.css('div.pagination--1bp3g').get()
                print("button", disabled_next_button)
                return disabled_next_button != None
  
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")


    def get_vehicle_info(self, response):
        try:
            vehicle_details = {}

            title = response.css(f"{self.title}::text").get()
            price = response.css(f"{self.price}::text").getall()
            table_rows = response.css(self.rows)

            if title:
                vehicle_details['title'] = title.strip()

            if len(price) == 2:
                vehicle_details['price'] = price[1].strip()

            for row in table_rows:
                key = row.css(f"{self.key}::text").get()
                value = row.css(f"{self.value}::text").get()
                if key and value:
                    vehicle_details[key.strip().replace(':', '')] = value.strip()

            print(f"{response.meta.get('index')}\t{response.url}")

        except Exception as e:
            err(f"{response.meta.get('index')}\t{response.url}\n{e}")


def run_scrapy():
    url = 'https://ikman.lk/en/ads/sri-lanka/cars?page=137'
    selectors = {
        'ads_link': 'div.result-img a',
        'next_button': 'ul.pages--2uPAr li:last-child',
        'title': 'h2.item-title',
        'price': 'p.m-0.col-6.col-sm-7.p-0.m-0 span',
        'rows': 'table.course-info tr',
        'key': 'td.w-25',
        'value': 'td.w-75'
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