from app.pipeline import run_pipeline
from app.storage.mongodb import ensure_indexes
from app.storage.subscriptions import ensure_subscription_indexes
from app.config import MONGO_URI, DB_NAME, COLLECTION_NAME

import asyncio

if __name__ == "__main__":
    ensure_indexes(MONGO_URI, DB_NAME, COLLECTION_NAME)
    ensure_subscription_indexes()

    asyncio.run(run_pipeline())
