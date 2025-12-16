import feedparser


def fetch_rss_articles(rss_feeds):
    articles = []

    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)

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
