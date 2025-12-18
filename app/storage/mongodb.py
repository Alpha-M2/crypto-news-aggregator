import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from datetime import datetime, timezone
from app.config import DB_NAME, COLLECTION_NAME
from app.logger import get_logger

logger = get_logger()

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set")


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

    return list(collection.find({}, {"_id": 0}).sort("created_at", -1).limit(limit))


def ensure_indexes(uri, db_name, collection_name):
    client = MongoClient(uri)
    collection = client[db_name][collection_name]

    collection.create_index("article_id", unique=True)


def fetch_undelivered_articles(since: datetime, limit=5):
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION_NAME]

    return list(
        collection.find({"created_at": {"$gt": since}}, {"_id": 0})
        .sort("created_at", 1)
        .limit(limit)
    )
