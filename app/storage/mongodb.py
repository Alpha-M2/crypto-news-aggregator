from pymongo import MongoClient
from pymongo.errors import BulkWriteError

from app.config import DB_NAME, COLLECTION_NAME
from app.logger import get_logger

logger = get_logger()


def save_articles(uri, db_name, collection_name, articles):
    if not articles:
        logger.warning("No articles to save")
        return

    client = MongoClient(uri)
    collection = client[db_name][collection_name]

    try:
        result = collection.insert_many(articles, ordered=False)
        logger.info(f"Inserted {len(result.inserted_ids)} articles")
    except BulkWriteError as e:
        logger.warning("Duplicate articles skipped during insert")


def fetch_articles(uri, db_name, collection_name, limit=20):
    client = MongoClient(uri)
    collection = client[db_name][collection_name]

    articles = list(collection.find({}, {"_id": 0}).sort("created_at", -1).limit(limit))

    return articles


def ensure_indexes(uri, db_name, collection_name):
    client = MongoClient(uri)
    collection = client[db_name][collection_name]

    collection.create_index("article_id", unique=True)
