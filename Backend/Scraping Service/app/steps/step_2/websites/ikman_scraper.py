import json
import re
from app.data.parameters import PRICE, CATEGORY
from .web_scraper import WebScraper


class IkmanScraper(WebScraper):

    def __init__(self, **kwargs):
        site_data = kwargs.get('site_data')
        selectors = site_data['selectors']
        name = site_data['name']
        self.banned_categories = site_data['banned_categories']
        self.category = selectors['category']
        self.price = selectors['price']
        self.title = selectors['title']
        self.table = selectors['table']
        super(IkmanScraper, self).__init__(name=name, **kwargs)

    def get_vehicle_info(self, response, vehicle_details):
        price = response.css(f"{self.price}::text").get()
        title = response.css(f'{self.title}::text').get()
        table = response.css(self.table)
        breadcrumb = response.css(f'{self.category}::text').getall()

        # Home > All Ads > Vehicles > category
        category = breadcrumb[3] if len(breadcrumb) > 3 else None

        if price and isinstance(price, str):
            vehicle_details[PRICE] = price.strip()

        if title and isinstance(title, str):
            vehicle_details['title'] = title.strip()

        if category and isinstance(category, str):
            category = category.strip()
            if category in self.banned_categories:
                raise RuntimeError(f"Banned Category")
            vehicle_details[CATEGORY] = category

        for row in table:
            key = self.get_key(row.css('div:nth-child(1)::text').get())
            value_el = row.css('div:nth-child(2)')
            value = value_el.css('div a span::text').get() or value_el.css('::text').get()

            if key and value and isinstance(value, str):
                vehicle_details[key] = value.strip()
            elif value == 'SUV / 4x4':
                vehicle_details[CATEGORY] = 'SUV'

        vehicle_details['image'] = self.get_image(response).strip()

        return vehicle_details


    @staticmethod
    def get_image(response) -> str:
        """
        Extract the first image URL from the Ikman ad page.
        """
        try:
            # Extract the JSON object from the embedded JavaScript
            # <script type="text/javascript">window.initialData = {};</script>
            script_data = re.search(
                r"window\.initialData\s*=\s*(\{.*?})\s*</script>",
                response.text,
                re.DOTALL
            )

            if not script_data:
                return ""

            # Parse JSON
            data = json.loads(script_data.group(1))

            # Navigate safely to the image
            ad = data.get("adDetail", {}).get("data", {}).get("ad", {})
            first_image_url = ad["images"]["meta"][0]["src"]
            return first_image_url + "/620/466/fitted.jpg"

        except (json.JSONDecodeError, KeyError, IndexError):
            return ""
