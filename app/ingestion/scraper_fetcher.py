import feedparser
from app.config import RSS_FEEDS


def fetch_scraped_articles(scrape_sources=RSS_FEEDS):
    """
    Fetch articles from RSS feeds.
    Maintains original structure of scraper_fetcher.py
    """
    articles = []

    for source in scrape_sources:
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries:
                articles.append(
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.get("published", ""),
                        "summary": entry.get("summary", ""),
                        "source": source["name"],
                    }
                )

            print(f"[INFO] Scraper initialized for {source['name']}")

        except Exception as e:
            print(f"[ERROR] Failed to scrape {source['name']}: {e}")

    return articles
