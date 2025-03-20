from app.utils.logger import info, warn, err
from app.steps.shared.site_data import riyasewana
from .web_scraper import WebScraper


class RiyasewanaScraper(WebScraper):

    def __init__(self, **kwargs):
        selectors = kwargs.get('site_data')['selectors']
        name = kwargs.get('site_data')['name']
        self.title = selectors['title']
        self.table = selectors['table']
        super(RiyasewanaScraper, self).__init__(name=name, **kwargs)


    def get_vehicle_info(self, response, vehicle_details):
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
                raise RuntimeError("Price is negotiable") 
            else:
                vehicle_details['price'] = price.strip()
        else:
            raise RuntimeError("Price not found")


        if title:
            vehicle_details['title'] = title.strip()
        else:
            raise RuntimeError("Title not found")


        for row in range(0, 4):
            for col in range(1, 4, 2):
                key = self.get_key(table[row].css(f"td:nth-child({col}) p::text").get())
                value = table[row].css(f"td:nth-child({col+1})::text").get()
                
                if key and value and isinstance(value, str):
                    vehicle_details[key] = value.strip()

        return vehicle_details
