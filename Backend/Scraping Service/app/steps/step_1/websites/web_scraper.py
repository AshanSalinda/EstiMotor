import scrapy

from app.config import settings
from app.db.repository.ad_links_repository import ad_links_repo
from app.utils.logger import err
from app.data.site_data import ikman


class WebScraper(scrapy.Spider):
    """Base class for website-specific scrapers"""

    def __init__(self, **kwargs):
        site_data = kwargs.get('site_data')
        self.progress_manager = kwargs.get('progress_manager')
        self.name = site_data['name']
        self.start_urls = [site_data['url']]
        self.page_no = site_data['page_no']
        self.ad_selector = site_data['selectors']['ads_link']
        self.ad_links = set()
        self.batch_size = settings.SCRAPING_BATCH_SIZE
        super(WebScraper, self).__init__()

    def start_requests(self):
        """Called when the spider starts crawling"""
        params = f"?page={self.page_no}" if self.page_no and self.page_no > 1 else ""

        for url in self.start_urls:
            yield scrapy.Request(
                url + params,
                callback=self.parse,
                meta={'index': f"{self.name}:{self.page_no}"}
            )

    def parse(self, response, **kwargs):
        """This is the default callback for every request for pages, made by the spider"""
        try:
            # Extract All Ad's links
            new_ad_links = response.css(f"{self.ad_selector}::attr(href)").getall()

            if self.name == ikman['name']:
                # ikman links missing the domain name
                new_ad_links = [response.urljoin(link) for link in new_ad_links]

            # accumulate all extracted new links
            self.ad_links.update(new_ad_links)

            # Handle pagination
            last_page = self.is_last_page(response)

            if last_page:
                # Save in db
                ad_links_repo.save(self.name, self.ad_links)

            else:
                # Save in db only if more than batch size
                if len(self.ad_links) > self.batch_size:
                    ad_links_repo.save(self.name, self.ad_links)
                    self.ad_links.clear()

                # next page
                yield self.navigate_to_next_page(response)

        except Exception as e:
            err(f"An error occurred during scraping: {e}")

    def navigate_to_next_page(self, response):
        next_page_url = ""
        try:
            self.page_no += 1
            next_page_url = f"{response.url.split('?')[0]}?page={self.page_no}"
            return response.follow(
                next_page_url,
                callback=self.parse,
                meta={'index': f"{self.name}:{self.page_no}"}
            )

        except Exception as e:
            err(f"Failed to navigate next page: {next_page_url}: {e}")

    def is_last_page(self, response):
        """
        is_last_page(self, response: scrapy.http.Response) -> bool

        Checks if the current page is the last page by looking for the pagination element 
        in the given response object.

        Args:
            response: The HTTP response object containing the content of the webpage.

        Returns:
            bool: True if  it's the last page; False otherwise.

        Raises:
            Exception: If an error occurs during the check, logs an error message with 
            this format.
            (f"Failed to check if it is_last_page for {response.url} \n {e}")
        """
        err(f"is_last_page method is not implemented in the child class: {self.name}")
        raise NotImplementedError(f"is_last_page method is not implemented in the child class: {self.name}")
