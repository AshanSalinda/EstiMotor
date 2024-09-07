import logging
from bs4 import BeautifulSoup
import requests

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



def scrape_patpat():
    page_no = 638
    all_vehicle_data = []

    while page_no > 0:
        logger.info(f"Scraping page no: {page_no}")

        page_data = get_page_data(str(page_no))
        page_no = 0 if page_data['is_last_page'] else page_no + 1
        vehicle_links = page_data['vehicle_links']
        
        for link in vehicle_links:
            logger.info(f"Scraping vehicle page: {link}")
            vehicle_data = scrape_vehicle_page(link)
            if vehicle_data:
                all_vehicle_data.append(vehicle_data)


    logger.info("Scraping completed.")
    print(all_vehicle_data)
    return all_vehicle_data



def get_page_data(page_no):
    try:    
        details_selector = 'div.result-img a'
        next_page_selector = 'ul.pagination li:last-child'
        BASE_URL = 'https://www.patpat.lk/vehicle?page='
        
        vehicle_links = []
        is_last_page = False

        response = requests.get(BASE_URL + page_no)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        next_page = soup.select_one(next_page_selector)
        if next_page:
            is_last_page = next_page.get('class') == ['disabled']

        for link in soup.select(details_selector):
            href = link.get('href')
            if href:
                vehicle_links.append(href)

        return {
            'is_last_page': is_last_page, 
            'vehicle_links': vehicle_links
        }

    except requests.RequestException as e:
        logger.error(f"Page Data Getting Error for: {BASE_URL + page_no} {e}", exc_info=True)
        return {'is_last_page': False, 'vehicle_links': []}



def scrape_vehicle_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        title_class = 'item-title'
        price_class = 'm-0 col-6 col-sm-7 p-0 m-0'
        table_class = 'course-info table table-striped'

        vehicle_details = {}


        title_container = soup.find('h2', class_ = title_class)
        if title_container:
            vehicle_details['title'] = title_container.get_text(strip=True)
        else:
            logger.warning("Title not found")


        price_container = soup.find('p', class_ = price_class)
        if price_container:
            price_spans = price_container.find_all('span')
            if len(price_spans) == 2:
                vehicle_details['price'] = price_spans[1].get_text(strip=True)
            else:
                logger.warning("Price span not found")


        table = soup.find('table', class_ = table_class)
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

        return vehicle_details


    except requests.RequestException as e:
        logger.error(f"Request failed: {e}", exc_info=True)
        return {}
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}", exc_info=True)
        return {}


if __name__ == '__main__':
    scrape_patpat()
