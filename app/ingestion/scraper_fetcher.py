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
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                logger.info(
                    f"Scraper initialized for {source['name']} ({source['url']})"
                )

                for link in soup.select("a"):
                    href = link.get("href")
                    text = link.get_text(strip=True)

                    if not href or not text or len(text) < 25:
                        continue

                    if not href.startswith("http"):
                        continue

                    articles.append(
                        {
                            "title": text,
                            "link": href,
                            "summary": "",
                            "source": source["name"],
                        }
                    )

                break  # success, stop retrying

            except requests.RequestException as e:
                attempt += 1
                logger.error(
                    f"Failed scraping {source['name']}: {e}, retry {attempt}/{retries}"
                )
                sleep(2)

    return articles
