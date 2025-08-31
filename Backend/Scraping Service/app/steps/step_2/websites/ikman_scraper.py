from app.data.parameters import PRICE, CATEGORY
from .web_scraper import WebScraper


class IkmanScraper(WebScraper):

    def __init__(self, **kwargs):
        selectors = kwargs.get('site_data')['selectors']
        name = kwargs.get('site_data')['name']
        self.category = selectors['category']
        self.price = selectors['price']
        self.table = selectors['table']
        super(IkmanScraper, self).__init__(name=name, **kwargs)

    def get_vehicle_info(self, response, vehicle_details):
        price = response.css(f"{self.price}::text").get()
        table = response.css(self.table)
        breadcrumb = response.css(f'{self.category}::text').getall()

        # Home > All Ads > Vehicles > category
        category = breadcrumb[3] if len(breadcrumb) > 3 else None

        vehicle_details[PRICE] = price
        vehicle_details[CATEGORY] = category

        for row in table:
            key = self.get_key(row.css('div:nth-child(1)::text').get())
            value_el = row.css('div:nth-child(2)')
            value = value_el.css('div a span::text').get() or value_el.css('::text').get()

            if key and value and isinstance(value, str):
                vehicle_details[key] = value.strip()

        return vehicle_details
