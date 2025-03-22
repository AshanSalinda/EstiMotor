from .web_scraper import WebScraper


class PatpatScraper(WebScraper):

    def __init__(self, **kwargs):
        selectors = kwargs.get('site_data')['selectors']
        name = kwargs.get('site_data')['name']
        self.title = selectors['title']
        self.price = selectors['price']
        self.rows = selectors['rows']
        super(PatpatScraper, self).__init__(name=name, **kwargs)

    def get_vehicle_info(self, response, vehicle_details):
        title = response.css(f"{self.title}::text").get()
        price = response.css(f"{self.price}::text").get()
        table = response.css(self.rows)

        if price:
            if price == 'Negotiable':
                raise RuntimeError("Price is negotiable")
            else:
                vehicle_details['price'] = price.strip()
        else:
            raise RuntimeError("Price not found")

        if title:
            vehicle_details['title'] = title.strip()
        else:
            raise RuntimeError("Title not found")

        for row in table:
            key = self.get_key(row.css('th::text').get())
            value = row.css('td::text').get()
            if key and value and isinstance(value, str):
                vehicle_details[key] = value.strip()

        return vehicle_details
