from app.utils.logger import err
from .web_scraper import WebScraper


class IkmanScraper(WebScraper):

    def __init__(self, **kwargs):
        self.pagination = kwargs.get('site_data')['selectors']['pagination']
        super(IkmanScraper, self).__init__(**kwargs)

    def is_last_page(self, response):
        try:
            # Extract the pagination element
            pagination = response.css(self.pagination).get()
            return pagination is None

        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")
