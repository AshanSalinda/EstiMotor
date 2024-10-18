from celery import Celery
from ..web_scraper.driver import start_scraping, stop_scraping

app = Celery('scraper', broker='redis://localhost:6379/0')

@app.task
def start_scraping_task():
    start_scraping()

@app.task
def stop_scraping_task():
    stop_scraping()
