from utils.logger import info, warn, err
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from ..spyder.web_scraper import WebScraper


class RiyasewanaScraper(WebScraper):
    name = "riyasewana_scraper"

    def __init__(self, url, selectors, *args, **kwargs):
        self.next_button = selectors['next_button']
        self.title = selectors['title']
        self.table = selectors['table']
        ad_selector = selectors['ads_link']
        super(RiyasewanaScraper, self).__init__(url, ad_selector, *args, **kwargs)


    def is_last_page(self, response):
        try:
            last_button_text = response.css(f"{self.next_button}::text").get()
            return last_button_text != "Next"
  
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")


    def get_vehicle_info(self, response):
        try:
            vehicle_details = {}

            title = response.css(f"{self.title}::text").get()
            table = response.css('table.moret tr')
            price = None

            # Remove unnecessary upper rows
            while price is None:
                tr1 = table.pop(0)
                key = tr1.css('td:nth-child(3) p::text').get()
                if key == 'Price':
                    price = tr1.css('td:nth-child(4) span::text').get().strip()


            if table[0].css('td:nth-child(1) p::text').get().strip() == 'Get Leasing':
                table.pop(0)
                

            if price:
                if price == 'Negotiable':
                    raise Exception("Price is negotiable") 
                else:
                    vehicle_details['price'] = price.strip()
            else:
                raise Exception("Price not found")


            if title:
                vehicle_details['title'] = title.strip()
            else:
                raise Exception("Title not found")


            for row in range(0, 4):
                for col in range(1, 4, 2):
                    key = table[row].css(f"td:nth-child({col}) p::text").get()
                    value = table[row].css(f"td:nth-child({col+1})::text").get()
                    
                    if key and value and type(key) == str and type(value) == str:
                        vehicle_details[key.strip()] = value.strip()



            print(f"{response.meta.get('index')}\t{response.url}")
            print(vehicle_details)

        except Exception as e:
            err(f"{response.meta.get('index')}\t{response.url}\n{e}")


def run_scrapy():
    url = 'https://riyasewana.com/search?page=1380'
    selectors = {
        'ads_link': 'ul li.item.round h2 a',
        'next_button': 'div.pagination a:last-of-type',
        'title': '#content h1',
        'table': 'table.moret tbody',
    }


    process = CrawlerProcess(settings={
        "LOG_LEVEL": 'WARNING',
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
        "BOT_NAME": 'EstiMotor_scraper',
        "USER_AGENT": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    })


    process.crawl(RiyasewanaScraper, url, selectors)
    process.start()


if __name__ == '__main__':
    run_scrapy()