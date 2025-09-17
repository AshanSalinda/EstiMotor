from app.utils.logger import err
from .web_scraper import WebScraper


class IkmanScraper(WebScraper):

    def __init__(self, **kwargs):
        self.pagination = kwargs.get('site_data')['selectors']['pagination']
        super(IkmanScraper, self).__init__(**kwargs)

    def is_last_page(self, response):
        try:
            # Extract numbers using Scrapy's re() on the CSS selector
            # Example pagination text: "Showing 76-100 of 82,684 ads"
            # This will Extract: ['76', '100', '82,684']
            numbers = response.css(f"{self.pagination}::text").re(r'[\d,]+')

            # Remove commas and convert to int
            numbers = list(map(lambda x: int(x.strip().replace(',', '')), numbers))

            if len(numbers) == 3:
                start, end, total = numbers
                page_no = response.url.split('page=')[-1]

                # If not first page but start resets to 1 → last page
                if start == 1 and page_no.isdigit() and int(page_no) > 1:
                    return True

                # Last page if end reaches total or start goes beyond total
                return end == total or start >= total

            return True  # If numbers are not as expected, assume last page

        except Exception as e:
            err(f"Failed to check if it is_last_page for {response.url} \n {e}")
