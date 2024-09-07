import logging
from bs4 import BeautifulSoup
import requests

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def scrape_patpat():
    url = 'https://www.patpat.lk/vehicle/car/Honda/City/2003/honda-city/1308414'
    priceClass = 'm-0 col-6 col-sm-7 p-0 m-0'
    tableClass = 'course-info table table-striped'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize vehicle details dictionary
        vehicle_details = {}

        # Extract vehicle price
        price_container = soup.find('p', class_ = priceClass)
        if price_container:
            price_spans = price_container.find_all('span')
            if len(price_spans) == 2:
                vehicle_details['price'] = price_spans[1].get_text(strip=True)
            else:
                logger.warning("Price span not found")

        # Extract vehicle details from the table
        table = soup.find('table', class_ = tableClass)
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].get_text(strip=True).replace(':', '')
                    value = cells[1].get_text(strip=True)
                    vehicle_details[key] = value
        else:
            logger.warning("Details table not found")

        # Print extracted details
        if vehicle_details:
            for key, value in vehicle_details.items():
                print(f"{key}: {value}")
        else:
            logger.info("No vehicle details found")

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}", exc_info=True)

if __name__ == '__main__':
    scrape_patpat()
