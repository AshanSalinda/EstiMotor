from app.data.parameters import PRICE
from .web_scraper import WebScraper


class PatpatScraper(WebScraper):

    def __init__(self, **kwargs):
        selectors = kwargs.get('site_data')['selectors']
        name = kwargs.get('site_data')['name']
        self.price = selectors['price']
        self.rows = selectors['rows']
        super(PatpatScraper, self).__init__(name=name, **kwargs)

    def get_vehicle_info(self, response, vehicle_details):
        price = response.css(f"{self.price}::text").get()
        table = response.css(self.rows)

        vehicle_details[PRICE] = price

        for row in table:
            key = self.get_key(row.css("div > span:last-child::text").get())
            value = row.xpath("span[not(parent::div)][1]/text()").get()

            if key and value and isinstance(value, str):
                vehicle_details[key] = value.strip()

        return vehicle_details
