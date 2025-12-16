from pymongo import MongoClient
from app.logger import get_logger

logger = get_logger()


def save_articles(uri, db_name, collection_name, articles):
    client = MongoClient(uri)
    collection = client[db_name][collection_name]

    for article in articles:
        # Use URL or title hash as unique identifier
        if collection.count_documents({"url": article.get("url")}, limit=1) == 0:
            collection.insert_one(article)
        else:
            logger.info(f"Duplicate skipped: {article.get('title')}")


def fetch_articles(uri, db_name, collection_name, limit=20):
    client = MongoClient(uri)
    collection = client[db_name][collection_name]

    articles = list(collection.find({}, {"_id": 0}).sort("created_at", -1).limit(limit))

    return articles
