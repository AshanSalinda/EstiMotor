from app.utils.logger import err
from .web_scraper import WebScraper


class IkmanScraper(WebScraper):

    def __init__(self, **kwargs):
        self.pagination = kwargs.get('site_data')['selectors']['pagination']
        super(IkmanScraper, self).__init__(**kwargs)

    def is_last_page(self, response):
        try:
            # Extract numbers using Scrapy's re() on the CSS selector
            # Example pagination text: "Showing 251-253 of 253 ads"
            # This will extract: ['251', '253', '253']
            numbers = response.css(f"{self.pagination}::text").re(r'\d+')

            if len(numbers) >= 3:
                start, end, total = map(int, numbers[:3])
                return end >= total

            return True  # If numbers are not as expected, assume last page

        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")
