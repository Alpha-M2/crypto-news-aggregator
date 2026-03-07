import asyncio
import aiohttp
from bs4 import BeautifulSoup

from app.logger import get_logger

logger = get_logger()


async def fetch_single_source(session, source, retries=3):
    attempt = 0
    articles = []

    while attempt < retries:
        try:
            async with session.get(source["url"], timeout=10) as response:
                response.raise_for_status()
                html = await response.text()

                soup = BeautifulSoup(html, "html.parser")
                logger.info(
                    f"Scraper initialized for {source['name']} ({source['url']})"
                )

                for link in soup.select("a"):
                    href = link.get("href")
                    text = link.get_text(strip=True)

                    if not href or not text or len(text) < 25:
                        continue

                    if not href.startswith("http"):
                        continue

                    articles.append(
                        {
                            "title": text,
                            "link": href,
                            "summary": "",
                            "source": source["name"],
                        }
                    )

                return articles

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            attempt += 1
            logger.error(
                f"Failed scraping {source['name']}: {e}, retry {attempt}/{retries}"
            )
            await asyncio.sleep(2)
            
        except Exception as e:
            logger.error(f"Unexpected error scraping {source['name']}: {e}")
            break

    return articles


async def fetch_scraped_articles_async(scrape_sources, retries=3):
    all_articles = []
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_single_source(session, source, retries) for source in scrape_sources
        ]
        
        results = await asyncio.gather(*tasks)
        for result in results:
            all_articles.extend(result)
            
    return all_articles


def fetch_scraped_articles(scrape_sources, retries=3):
    # Synchronous wrapper for backward compatibility or direct pipeline usage
    return asyncio.run(fetch_scraped_articles_async(scrape_sources, retries))
