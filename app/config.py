import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI")

DB_NAME = "crypto_news"
COLLECTION_NAME = "articles"


RSS_FEEDS = [
    "https://cryptonews.com/news/feed/",
    "https://cointelegraph.com/rss",
    "https://news.bitcoin.com/feed/",
    "https://messari.io/rss",
    "https://cryptorank.io/rss",
    "https://www.todayonchain.com/rss",
    "https://www.coingecko.com/en/rss",
    "https://coinmarketcap.com/headlines/rss",
]

SCRAPE_SOURCES = [
    {"name": "Messari", "url": "https://messari.io/news"},
    {"name": "CryptoRank", "url": "https://cryptorank.io/news"},
    {"name": "TodayOnChain", "url": "https://www.todayonchain.com/news/"},
    {"name": "CoinGecko", "url": "https://www.coingecko.com/en/news"},
    {"name": "CoinMarketCap", "url": "https://coinmarketcap.com/headlines/news/"},
]

COINS = ["BTC", "Bitcoin", "ETH", "Ethereum", "SOL", "Solana"]
