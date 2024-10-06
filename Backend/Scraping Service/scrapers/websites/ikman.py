from bs4 import BeautifulSoup
import requests


def scrape_ikman():
    url = 'https://riyasewana.com/search?page=2'
    price_container_class = 'amount--3NTpl'
    details_container_class = 'ad-meta--17Bqm'
    label_div_class = 'word-break--2nyVq label--3oVZK'
    value_div_class = 'word-break--2nyVq value--1lKHt'
    next_button_class = 'pagination'

    try:
        url = 'https://riyasewana.com/search?page=2'
        response = requests.get(url, headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        })
        
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize vehicle details dictionary
        vehicle_details = {}

        next_button = soup.find('div', class_ = next_button_class)
        if next_button:
            print("Next page button found", next_button)
        else:
            print("Next page button not found")

        # # Extract vehicle price
        # price_container = soup.find('div', class_ = price_container_class)
        # if price_container:
        #    vehicle_details['price'] = price_container.get_text(strip=True)
        # else:
        #     print("Price not found")

        # # Find the details container
        # details_container = soup.find('div', class_ = details_container_class )
        # if details_container:
        #     # Iterate over each detail row
        #     detail_rows = details_container.find_all('div', class_='full-width--XovDn')
        #     for row in detail_rows:
        #         label_div = row.find('div', class_ = label_div_class)
        #         value_div = row.find('div', class_= value_div_class)
        #         if label_div and value_div:
        #             label = label_div.get_text(strip=True).replace(':', '')
        #             # Handle cases where the value is wrapped in another tag
        #             value = value_div.get_text(strip=True)
        #             vehicle_details[label] = value
        # else:
        #     print("Details table not found")

        # # Print extracted details
        # if vehicle_details:
        #     for key, value in vehicle_details.items():
        #         print(f"{key}: {value}")
        # else:
        #     print("No vehicle details found")

    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred during scraping: {e}")

if __name__ == '__main__':
    scrape_ikman()
