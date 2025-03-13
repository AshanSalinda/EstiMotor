from app.utils.logger import info, warn, err
from app.steps.site_data import ikman
from .web_scraper import WebScraper


class IkmanScraper(WebScraper):
    name = "ikman"

    def __init__(self):
        selectors = ikman['selectors']
        url = ikman['url']
        page_no = ikman['page_no']
        ad_selector = selectors['ads_link']
        self.pagination = selectors['pagination']
        super(IkmanScraper, self).__init__(url, page_no, ad_selector)


    def is_last_page(self, response):
        try:
            # Extract the pagination element
            pagination = response.css(self.pagination).get()
            return pagination == None
  
        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")