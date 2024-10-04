# from scrapers.patpat_scraper import scrape_patpat
from scrapers.ikman_scraper import scrape_ikman
from scrapers.web_scraper import scrape_patpat


def main():
    print("Starting the scraping service...")
    try:
        scrape_patpat()
        # scrape_ikman()
        print("Scraping completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
