from dotenv import load_dotenv

load_dotenv()

RSS_FEEDS = [
    "https://cryptonews.com/news/feed/",
    "https://cointelegraph.com/rss",
    "https://news.bitcoin.com/feed/",
]

SCRAPE_SOURCES = [
    {"name": "Messari", "url": "https://messari.io/news"},
    {"name": "CryptoRank", "url": "https://cryptorank.io/news"},
    {"name": "TodayOnChain", "url": "https://www.todayonchain.com/news/"},
    {"name": "CoinGecko", "url": "https://www.coingecko.com/en/news"},
    {"name": "CoinMarketCap", "url": "https://coinmarketcap.com/headlines/news/"},
]

COINS = ["BTC", "Bitcoin", "ETH", "Ethereum", "SOL", "Solana"]

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "crypto_news"
COLLECTION_NAME = "articles"
