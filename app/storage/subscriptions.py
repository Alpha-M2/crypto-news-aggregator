from pymongo import MongoClient
from app.config import MONGO_URI, DB_NAME
from datetime import datetime, timezone

COLLECTION = "subscriptions"


def ensure_subscription_indexes():
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION]

    collection.create_index("chat_id", unique=True)
    collection.create_index("active")


def activate_subscription(chat_id: int):
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION]

    collection.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "active": True,
                "updated_at": datetime.now(timezone.utc),
            }
        },
        upsert=True,
    )


def deactivate_subscription(chat_id: int):
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION]

    collection.update_one(
        {"chat_id": chat_id},
        {
            "$set": {
                "active": False,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )


def get_active_subscriptions():
    client = MongoClient(MONGO_URI)
    collection = client[DB_NAME][COLLECTION]

    return list(collection.find({"active": True}))
