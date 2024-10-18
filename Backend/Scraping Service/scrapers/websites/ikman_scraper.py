from utils.logger import info, warn, err
from ..web_scraper import WebScraper
from .site_data import ikman


class IkmanScraper(WebScraper):
    name = "ikman"

    def __init__(self):
        selectors = ikman['selectors']
        url = ikman['url']
        page_no = ikman['page_no']
        ad_selector = selectors['ads_link']
        self.pagination = selectors['pagination']
        self.title = selectors['title']
        self.price = selectors['price']
        self.table = selectors['table']
        super(IkmanScraper, self).__init__(url, page_no, ad_selector)


    def is_last_page(self, response):
        try:
            # Extract the pagination element
            pagination = response.css(self.pagination).get()
            return pagination == None
  
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")


    def get_vehicle_info(self, response, vehicle_details):
        title = response.css(f"{self.title}::text").get()
        price = response.css(f"{self.price}::text").get()
        table = response.css(self.table)

        if price and type(price) == str:
            vehicle_details['price'] = price.strip()

        if title and type(title) == str:
            vehicle_details['title'] = title.strip()

        for row in table:
            key = self.get_key(row.css('div:nth-child(1)::text').get())
            value_el = row.css('div:nth-child(2)')
            value = value_el.css('div a span::text').get() or value_el.css('::text').get()

            if key and value and type(value) == str:
                vehicle_details[key] = value.strip()

        return vehicle_details