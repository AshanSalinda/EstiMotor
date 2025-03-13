from app.utils.logger import info, warn, err
from app.steps.site_data import patpat
from .web_scraper import WebScraper


class PatpatScraper(WebScraper):
    name = "patpat"

    def __init__(self):
        selectors = patpat['selectors']
        url = patpat['url']
        page_no = patpat['page_no']
        ad_selector = selectors['ads_link']
        self.next_button = selectors['next_button']
        super(PatpatScraper, self).__init__(url, page_no, ad_selector)


    def is_last_page(self, response):
        try:
            disabled_next_button = response.css(self.next_button).get()
            return disabled_next_button != None
        
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")