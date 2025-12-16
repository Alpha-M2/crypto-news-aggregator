from app.config import (
    RSS_FEEDS,
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    SCRAPE_SOURCES,
    COINS,
)
from app.ingestion.rss_fetcher import fetch_rss_articles
from app.ingestion.scraper_fetcher import fetch_scraped_articles
from app.ingestion.api_fetcher import fetch_api_articles
from app.processing.filter import filter_by_coin
from app.processing.summarizer import summarize_articles
from app.storage.mongodb import save_articles
from app.logger import get_logger

logger = get_logger()
logger.info("Pipeline started")
logger.error("Error scraping source X")


def run_pipeline():
    rss_articles = fetch_rss_articles(RSS_FEEDS)
    scraped_articles = fetch_scraped_articles(SCRAPE_SOURCES)
    api_articles = fetch_api_articles()

    all_articles = rss_articles + scraped_articles + api_articles

    filtered = filter_by_coin(all_articles, COINS)
    summarized = summarize_articles(filtered)

    save_articles(MONGO_URI, DB_NAME, COLLECTION_NAME, summarized)
