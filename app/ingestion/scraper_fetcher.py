import requests
from bs4 import BeautifulSoup


def fetch_scraped_articles(scrape_sources):
    """
    Generic scraper framework.
    Site specific parsing will be added incrementally.
    """
    articles = []

    for source in scrape_sources:
        try:
            response = requests.get(source["url"], timeout=10)
            BeautifulSoup(response.text, "html.parser")

            print(f"[INFO] Scraper stub initialized for {source['name']}")

        except Exception as e:
            print(f"[ERROR] Failed to scrape {source['name']}: {e}")

    return articles
