from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")


def summarize_articles(articles):
    summarized = []

    for article in articles:
        try:
            summary = summarizer(
                article["summary"], max_length=60, min_length=25, do_sample=False
            )[0]["summary_text"]
        except Exception:
            summary = article["summary"][:150]

        summarized.append(
            {
                "title": article["title"],
                "link": article["link"],
                "summary": summary,
                "source": article["source"],
            }
        )

    return summarized
