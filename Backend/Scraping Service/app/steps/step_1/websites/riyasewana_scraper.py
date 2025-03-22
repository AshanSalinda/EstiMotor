from app.utils.logger import err
from .web_scraper import WebScraper


class RiyasewanaScraper(WebScraper):
    def __init__(self, **kwargs):
        selectors = kwargs.get('site_data')['selectors']
        self.next_button = selectors['next_button']
        self.current_button = selectors['current_button']
        super(RiyasewanaScraper, self).__init__(**kwargs)

    def is_last_page(self, response):
        try:
            requested_page = response.url.split('page=')[-1] if 'page=' in response.url else '1'
            last_button_text = response.css(f"{self.next_button}::text").get()
            current_button_text = response.css(f"{self.current_button}::text").get()
            return requested_page != current_button_text or last_button_text != "Next"

        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")
