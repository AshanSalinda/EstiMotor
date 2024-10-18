from ...utils.logger import info, warn, err
from ..web_scraper import WebScraper
from .site_data import riyasewana


class RiyasewanaScraper(WebScraper):
    name = "riyasewana"

    def __init__(self):
        selectors = riyasewana['selectors']
        self.next_button = selectors['next_button']
        self.title = selectors['title']
        self.table = selectors['table']
        ad_selector = selectors['ads_link']
        url = riyasewana['url']
        page_no = riyasewana['page_no']
        super(RiyasewanaScraper, self).__init__(url, page_no, ad_selector)


    def is_last_page(self, response):
        try:
            last_button_text = response.css(f"{self.next_button}::text").get()
            return last_button_text != "Next"
  
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")


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
                key = self.get_key(table[row].css(f"td:nth-child({col}) p::text").get())
                value = table[row].css(f"td:nth-child({col+1})::text").get()
                
                if key and value and type(value) == str:
                    vehicle_details[key] = value.strip()

        return vehicle_details
