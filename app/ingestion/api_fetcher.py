async def fetch_api_articles_async():
    """
    Stub for future API integrations:
    CoinMarketCap
    CoinGecko
    Messari
    """
    return []

def fetch_api_articles():
    import asyncio
    return asyncio.run(fetch_api_articles_async())
