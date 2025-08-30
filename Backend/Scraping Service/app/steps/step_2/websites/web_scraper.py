import scrapy

from app.data.parameters import *
from app.utils.logger import err


class WebScraper(scrapy.Spider):
    """Base class for website-specific scrapers"""

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.storage = kwargs.get('storage')
        self.start_urls = kwargs.get('links')
        self.scraped_data = kwargs.get('scraped_data')
        super(WebScraper, self).__init__()

    def start_requests(self):
        """Called when the spider starts crawling"""
        for index, url in enumerate(self.start_urls):
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={'index': f"{self.name}:{index + 1}"}
            )

    def parse(self, response, **kwargs):
        """This is the default callback for every request for pages, made by the spider"""
        index = ""
        url = ""
        try:
            url = response.url
            index = response.meta.get('index')
            vehicle_details = self.get_vehicle_info(response, {'url': url, 'index': index})
            self.scraped_data.append(vehicle_details)
            # self.storage.add(vehicle_details)

        except Exception as e:
            err(f"{index}\t{url}\t{e}")

    @staticmethod
    def get_key(key):
        keys = {
            'Brand:': MAKE,
            'Manufacturer': MAKE,
            'Make': MAKE,
            'Model:': MODEL,
            'Model': MODEL,
            'Year of Manufacture:': YOM,
            'Model Year': YOM,
            'YOM': YOM,
            'Transmission:': TRANSMISSION,
            'Transmission': TRANSMISSION,
            'Gear': TRANSMISSION,
            'Engine capacity:': ENGINE_CAPACITY,
            'Engine Capacity': ENGINE_CAPACITY,
            'Engine (cc)': ENGINE_CAPACITY,
            'Fuel type:': FUEL_TYPE,
            'Fuel Type': FUEL_TYPE,
            'Mileage:': MILEAGE,
            'Mileage': MILEAGE,
            'Mileage (km)': MILEAGE,
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
