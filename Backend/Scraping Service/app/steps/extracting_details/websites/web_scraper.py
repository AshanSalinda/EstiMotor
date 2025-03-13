import scrapy
from app.utils.logger import err


class WebScraper(scrapy.Spider):
    """Base class for website-specific scrapers"""
    def __init__(self, *args):
        super(WebScraper, self).__init__()
        self.start_urls = [args[0]]
        self.page_no = args[1]
        self.ad_selector = args[2]
        self.ad_links = set()


    def start_requests(self):
        """Called when the spider starts crawling"""
        for url in self.start_urls:
            yield scrapy.Request(
                f"{url}?page={self.page_no}", 
                callback=self.parse,
                meta={'index': f"{self.name}:{self.page_no}"}
            )


    def parse(self, response):
        """This is the default callback for every request for pages, made by the spider"""
        try:
            # Extract All Ad's links
            new_links = response.css(f"{self.ad_selector}::attr(href)").getall()
            self.ad_links.update(new_links)
                        
            # Handle pagination
            last_page = self.is_last_page(response)
            if not last_page:
                yield self.navigate_to_next_page(response)
                
        
        except Exception as e:
            err(f"An error occurred during scraping: {e}")

    
    def navigate_to_next_page(self, response):
        try:
            self.page_no += 1
            next_page_url = f"{(response.url).split('?')[0]}?page={self.page_no}"
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