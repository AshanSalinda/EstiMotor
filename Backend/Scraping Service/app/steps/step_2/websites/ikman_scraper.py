from app.utils.logger import info, warn, err
from .web_scraper import WebScraper


class IkmanScraper(WebScraper):
    
    def __init__(self, **kwargs):
        selectors = kwargs.get('site_data')['selectors']
        name = kwargs.get('site_data')['name']
        self.title = selectors['title']
        self.price = selectors['price']
        self.table = selectors['table']
        super(IkmanScraper, self).__init__(name=name, **kwargs)


    def get_vehicle_info(self, response, vehicle_details):
        title = response.css(f"{self.title}::text").get()
        price = response.css(f"{self.price}::text").get()
        table = response.css(self.table)

        if price and isinstance(price, str):
            vehicle_details['price'] = price.strip()
        else:
            raise RuntimeError("Price not found")

        if title and isinstance(title, str):
            vehicle_details['title'] = title.strip()
        else:
            raise RuntimeError("Title not found")

        for row in table:
            key = self.get_key(row.css('div:nth-child(1)::text').get())
            value_el = row.css('div:nth-child(2)')
            value = value_el.css('div a span::text').get() or value_el.css('::text').get()

            if key and value and isinstance(value, str):
                vehicle_details[key] = value.strip()

        return vehicle_details