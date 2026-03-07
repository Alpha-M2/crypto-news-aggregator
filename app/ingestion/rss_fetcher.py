import asyncio
import aiohttp
import feedparser

from app.logger import get_logger

logger = get_logger()


async def fetch_single_rss(session, feed_url):
    articles = []
    try:
        async with session.get(feed_url, timeout=10) as response:
            response.raise_for_status()
            xml_content = await response.text()
            
            # Since feedparser doesn't do async network IO natively when given a string, 
            # parsing the string is fast and non-blocking enough here.
            feed = feedparser.parse(xml_content)

            for entry in feed.entries:
                articles.append(
                    {
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "summary": entry.get("summary", ""),
                        "source": feed_url,
                    }
                )
            
            return articles
            
    except Exception as e:
        logger.error(f"Failed fetching RSS feed {feed_url}: {e}")
        return []


async def fetch_rss_articles_async(rss_feeds):
    all_articles = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_single_rss(session, url) for url in rss_feeds]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            all_articles.extend(result)
            
    return all_articles


def fetch_rss_articles(rss_feeds):
    return asyncio.run(fetch_rss_articles_async(rss_feeds))
