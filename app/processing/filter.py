def filter_by_coin(articles, coins):
    filtered = []

    for article in articles:
        text = f"{article['title']} {article['summary']}".lower()

        if any(coin.lower() in text for coin in coins):
            filtered.append(article)

    return filtered
