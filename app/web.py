from app.storage.mongodb import fetch_articles
from app.config import MONGO_URI, DB_NAME, COLLECTION_NAME

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/articles", methods=["GET"])
def get_articles():
    articles = fetch_articles(
        uri=MONGO_URI, db_name=DB_NAME, collection_name=COLLECTION_NAME, limit=20
    )
    return jsonify(articles), 200


if __name__ == "__main__":
    app.run(debug=True)
