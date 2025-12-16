from pymongo import MongoClient


def save_articles(uri, db_name, collection_name, articles):
    client = MongoClient(uri)
    collection = client[db_name][collection_name]

    if articles:
        collection.insert_many(articles)
