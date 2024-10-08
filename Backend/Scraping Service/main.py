from scrapers.websites.riyasewana_scraper import run_scrapy
# from scrapers.websites.ikman_scraper import run_scrapy
# from scrapers.websites.patpat_scraper import run_scrapy


def main():
    print("Starting the scraping service...")
    try:
        # scrape_patpat()
        # scrape_ikman()
        run_scrapy()
        print("Scraping completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
