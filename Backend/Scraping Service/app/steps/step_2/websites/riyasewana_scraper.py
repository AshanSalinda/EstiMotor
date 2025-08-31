from app.data.parameters import PRICE, CATEGORY
from .web_scraper import WebScraper


class RiyasewanaScraper(WebScraper):

    def __init__(self, **kwargs):
        selectors = kwargs.get('site_data')['selectors']
        name = kwargs.get('site_data')['name']
        self.category = selectors['category']
        self.table = selectors['table']
        super(RiyasewanaScraper, self).__init__(name=name, **kwargs)

    def get_vehicle_info(self, response, vehicle_details):
        table = response.css(self.table[0])

        is_desktop_response = True

        if not table:
            is_desktop_response = False
            table = response.css(self.table[1])

        if is_desktop_response:
            price = None

            # Remove unnecessary upper rows
            while price is None:
                if not table:
                    print(response.body.decode())
                tr1 = table.pop(0)
                key = tr1.css('td:nth-child(3) p::text').get()
                if key == 'Price':
                    price = tr1.css('td:nth-child(4) span::text').get().strip()

            if table[0].css('td:nth-child(1) p::text').get().strip() == 'Get Leasing':
                table.pop(0)

            if isinstance(price, str):
                vehicle_details[PRICE] = price.strip()

            for row in range(0, 4):
                for col in range(1, 4, 2):
                    key = self.get_key(table[row].css(f"td:nth-child({col}) p::text").get())
                    value = table[row].css(f"td:nth-child({col + 1})::text").get()

                    if key and value and isinstance(value, str):
                        vehicle_details[key] = value.strip()

        else:
            for row in table:
                key_text = row.css('p::text').get()
                value = row.xpath('p/following-sibling::text()[1]').get() or ""

                if key_text == 'Price' and isinstance(value, str):
                    vehicle_details[PRICE] = value.strip()
                    continue
                else:
                    key = self.get_key(key_text)

                    if key and value and isinstance(value, str):
                        vehicle_details[key] = value.strip()

        vehicle_details[CATEGORY] = self.get_category(is_desktop_response, response)

        return vehicle_details


    def get_category(self, is_desktop, response):
        category = None
        try:
            # Extract link depending on device
            if is_desktop:
                link = response.css(f"{self.category[0]}::attr(href)").get()
            else:
                link = response.css(f"{self.category[1]}::attr(href)").get()

            if link and isinstance(link, str):
                link = link.strip()
                link = link.replace("//riyasewana.com/search/", "")
                category = link.split('/')[0]

            return category

        except (AttributeError, IndexError):
            pass

        return category
