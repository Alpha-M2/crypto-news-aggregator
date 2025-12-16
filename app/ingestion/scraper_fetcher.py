import requests
from bs4 import BeautifulSoup
from time import sleep
from app.logger import get_logger

logger = get_logger()


def fetch_scraped_articles(scrape_sources, retries=3):
    articles = []

    for source in scrape_sources:
        attempt = 0
        while attempt < retries:
            try:
                response = requests.get(source["url"], timeout=10)
                BeautifulSoup(response.text, "html.parser")
                logger.info(f"Scraper initialized for {source['name']}")
                break
            except requests.RequestException as e:
                attempt += 1
                logger.error(
                    f"Failed scraping {source['name']}: {e}, retry {attempt}/{retries}"
                )
                sleep(2)
    return articles
