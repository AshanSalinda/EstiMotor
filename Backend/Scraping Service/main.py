from scrapers.driver import run_scrapy


def main():
    print("Starting the scraping service...")
    try:
        run_scrapy()
        print("Scraping completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
