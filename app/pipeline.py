import hashlib
from datetime import datetime, timezone

from app.config import (
    RSS_FEEDS,
    MONGO_URI,
    DB_NAME,
    COLLECTION_NAME,
    SCRAPE_SOURCES,
    COINS,
)
from app.storage.mongodb import ensure_indexes

from app.ingestion.rss_fetcher import fetch_rss_articles
from app.ingestion.scraper_fetcher import fetch_scraped_articles
from app.ingestion.api_fetcher import fetch_api_articles
from app.processing.filter import filter_by_coin
from app.processing.summarizer import summarize_articles
from app.storage.mongodb import save_articles
from app.logger import get_logger

logger = get_logger()


def generate_article_id(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def normalize_articles(raw_articles):
    normalized = []

    for raw in raw_articles:
        url = raw.get("link") or raw.get("url")
        if not url:
            continue

        article = {
            "article_id": generate_article_id(url),
            "title": raw.get("title", ""),
            "url": url,
            "summary": raw.get("summary", ""),
            "source": raw.get("source", ""),
            "created_at": datetime.now(timezone.utc),
        }

        normalized.append(article)

    return normalized


def run_pipeline():
    logger.info("Pipeline run started")

    ensure_indexes(MONGO_URI, DB_NAME, COLLECTION_NAME)

    rss_articles = fetch_rss_articles(RSS_FEEDS)
    logger.info(f"RSS articles fetched: {len(rss_articles)}")

    scraped_articles = fetch_scraped_articles(SCRAPE_SOURCES)
    logger.info(f"Scraped articles fetched: {len(scraped_articles)}")

    api_articles = fetch_api_articles()
    logger.info(f"API articles fetched: {len(api_articles)}")

    raw_articles = rss_articles + scraped_articles + api_articles
    logger.info(f"Total raw articles: {len(raw_articles)}")

    if not raw_articles:
        logger.warning("No raw articles fetched, exiting pipeline")
        return

    normalized_articles = normalize_articles(raw_articles)
    logger.info(f"Normalized articles: {len(normalized_articles)}")

    if not normalized_articles:
        logger.warning("No articles after normalization, exiting pipeline")
        return

    if COINS:
        filtered_articles = filter_by_coin(normalized_articles, COINS)
        logger.info(f"Articles after coin filter: {len(filtered_articles)}")
    else:
        filtered_articles = normalized_articles
        logger.info("Coin filter disabled, using all articles")

    if not filtered_articles:
        logger.warning("No articles after filtering, exiting pipeline")
        return

    summarized_articles = summarize_articles(filtered_articles)
    logger.info(f"Summarized articles: {len(summarized_articles)}")

    if summarized_articles:
        save_articles(MONGO_URI, DB_NAME, COLLECTION_NAME, summarized_articles)
        logger.info(f"Articles saved to DB: {len(summarized_articles)}")
    else:
        logger.warning(
            "Summarizer returned no articles; saving normalized articles instead"
        )
        save_articles(MONGO_URI, DB_NAME, COLLECTION_NAME, filtered_articles)
        logger.info(f"Articles saved to DB: {len(filtered_articles)}")

    logger.info("Pipeline run completed")
