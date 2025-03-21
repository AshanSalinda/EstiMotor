import scrapy
from app.utils.logger import info, warn, err
from app.utils.storage import Storage
from datetime import datetime, timezone


# custom signal for indicate that reached to the end of pagination
pagination_ended_signal = object()


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

            else:
                # Send signal when pagination ends with the count of ads
                self.crawler.signals.send_catch_log(
                    signal=pagination_ended_signal, 
                    spider=self, 
                    data={'ads_count': len(self.ad_links)}
                )
                
                for index, link in enumerate(self.ad_links):
                    yield response.follow(
                        link, 
                        callback=self.process_the_ad, 
                        meta={'index': f"{self.name}:{index + 1}"}
                    )
        
        except Exception as e:
            err(f"An error occurred during scraping: {e}")

    
    def navigate_to_next_page(self, response):
        try:
            self.page_no += 1
            next_page_url = f"{(response.url).split('?')[0]}?page={self.page_no}"
            return response.follow(next_page_url, callback=self.parse)
        
        except Exception as e:
            err(f"Failed to navigate next page: {next_page_url}: {e}")	


    def process_the_ad(self, response):
        try:
            url = response.url
            index = response.meta.get('index')
            vehicle_details = self.get_vehicle_info(response, {'url': url, 'index': index})
            Storage.add_vehicle(vehicle_details)
            print(f"{index}\t{url}")
        
        except Exception as e:
            err(f"{index}\t{url}\t{e}")
            
    
    def get_key(self, key):
        keys = {
            'Brand:': 'Make',
            'Manufacturer': 'Make',
            'Make': 'Make',
            'Model:': 'Model',
            'Model': 'Model',
            'Year of Manufacture:': 'YOM',
            'Model Year': 'YOM',
            'YOM': 'YOM',
            'Transmission:': 'Transmission',
            'Transmission': 'Transmission',
            'Gear': 'Transmission',
            'Engine capacity:': 'Engine Capacity',
            'Engine Capacity': 'Engine Capacity',
            'Engine (cc)': 'Engine Capacity',
            'Fuel type:': 'Fuel type',
            'Fuel Type': 'Fuel Type',
            'Mileage:': 'Mileage',
            'Mileage': 'Mileage',
            'Mileage (km)': 'Mileage',
        } 

        key = key.strip() if key and isinstance(key, str) else None
        return keys.get(key)


    def get_vehicle_info(self, response, vehicle_details):
        """
        get_vehicle_info(self, response: scrapy.http.Response, vehicle_details: dict) -> dict

        Extracts vehicle information from the provided response object and return the updated vehicle_details dictionary.

        Args:
            response: The HTTP response containing the webpage's content for a vehicle ad.
            vehicle_details: A dictionary to store extracted vehicle information 

        Returns:
            dict: Updated vehicle_details dictionary containing the extracted data.
            {   
                url: Provided,
                index: Provided,
                Price: Must Include,
                Title: Must Include,
                Make: Must Include,
                Model: Must Include,
                YOM: Must Include,
                Transmission: Must Include,
                Engine Capacity: Must Include,
                Fuel type: Must Include,
                Mileage: Must Include,
            }

        Raises:
            No need to handle any exceptions here.
        """
        err(f"{self.name} must implement a own get_vehicle_info method")


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
        err(f"{self.name} must implement a own is_last_page method")


