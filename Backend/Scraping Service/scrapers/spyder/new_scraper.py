from utils.logger import info, warn, err
from bs4 import BeautifulSoup
from datetime import datetime
import requests


class NewScraper:
    def __init__(self, url, ad_url_selector, next_button_selector, get_vehicle_info):
        self.url = url
        self.ad_url_selector = ad_url_selector
        self.next_button_selector = next_button_selector
        self.get_vehicle_info = get_vehicle_info
        self.started_at = datetime.now()


    def scrape(self):
        try:       
            page_no = 570
            page_count = 0
            all_vehicle_data = []

            while page_no > 0:
                info(f"Scraping page no: {page_no}")

                page_info = self.get_page_info(str(page_no))
                page_no = 0 if page_info['is_last_page'] else page_no + 1
                # ad_links = page_info['ad_links']
                page_count += 1
                
                # for ad in ad_links:
                #     print(f"Scraping: {ad}")
                #     vehicle_data = self.get_vehicle_info(ad)

                #     if vehicle_data:
                #         all_vehicle_data.append(vehicle_data)

            info(f"Scraping completed in {datetime.now() - self.started_at}")
            return page_count

        except requests.RequestException as e:
            err(f"Request failed: {e}")
        except Exception as e:
            err(f"An error occurred during scraping: {e}")


    def get_page_info(self, page_no):
        try:
            ad_links = []
            is_last_page = False

            response = requests.get(self.url + page_no)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            next_button = soup.select_one(self.next_button_selector)

            if next_button:
                is_last_page = next_button.get('class') == ['disabled']

            # for ad in soup.select(self.ad_url_selector):
            #     href = ad.get('href')
            #     if href:
            #         ad_links.append(href)

            return {
                'is_last_page': is_last_page,
                'ad_links': ad_links
            }

        except requests.RequestException as e:
            err(f"Request failed: {e}")
        except Exception as e:
            err(f"An error occurred during scraping: {e}")


    def get_vehicle_info(self, url):
        try:
           raise NotImplementedError("Subclasses must implement this method")

        except requests.RequestException as e:
            err(f"Request failed: {e}")
        except Exception as e:
            err(f"An error occurred during scraping: {e}")


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
            print("Title not found")


        price_container = soup.find('p', class_ = price_class)
        if price_container:
            price_spans = price_container.find_all('span')
            if len(price_spans) == 2:
                vehicle_details['price'] = price_spans[1].get_text(strip=True)
            else:
                print("Price span not found")


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
            print("Details table not found")

        return vehicle_details


    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return {}


def scrape_patpat():
    url = 'https://www.patpat.lk/vehicle?page='
    ad_link_selector = 'div.result-img a'
    next_button_selector = 'ul.pagination li:last-child'
    get_vehicle_info = scrape_vehicle_page

    patpat_scraper = WebScraper(url, ad_link_selector, next_button_selector, get_vehicle_info)
    page_count = patpat_scraper.scrape()
    info(f"Scraped {page_count} pages")


if __name__ == '__main__':
    scrape_patpat()

