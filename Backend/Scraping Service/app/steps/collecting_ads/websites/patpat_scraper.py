from app.utils.logger import info, warn, err
from app.steps.shared.site_data import patpat
from .web_scraper import WebScraper


class PatpatScraper(WebScraper):
    
    def __init__(self, **kwargs):
        self.next_button = kwargs.get('site_data')['selectors']['next_button']
        super(PatpatScraper, self).__init__(**kwargs)


    def is_last_page(self, response):
        try:
            disabled_next_button = response.css(self.next_button).get()
            return disabled_next_button != None
        
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")
            