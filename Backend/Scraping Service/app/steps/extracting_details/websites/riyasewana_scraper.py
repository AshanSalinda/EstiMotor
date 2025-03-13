from app.utils.logger import info, warn, err
from app.steps.site_data import riyasewana
from .web_scraper import WebScraper


class RiyasewanaScraper(WebScraper):
    name = "riyasewana"

    def __init__(self):
        selectors = riyasewana['selectors']
        self.next_button = selectors['next_button']
        self.current_button = selectors['current_button']
        ad_selector = selectors['ads_link']
        url = riyasewana['url']
        page_no = riyasewana['page_no']
        super(RiyasewanaScraper, self).__init__(url, page_no, ad_selector)


    def is_last_page(self, response):
        try:
            requested_page = response.url.split('page=')[-1] if 'page=' in response.url else '1'
            last_button_text = response.css(f"{self.next_button}::text").get()
            current_button_text = response.css(f"{self.current_button}::text").get()
            return requested_page != current_button_text or last_button_text != "Next"
  
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")