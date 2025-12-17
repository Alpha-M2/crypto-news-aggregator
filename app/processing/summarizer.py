from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", device=0)


def summarize_articles(articles):
    summarized = []

    for article in articles:
        text = article.get("summary") or article.get("title", "")

        if len(text.split()) < 30:
            summarized.append(article)
            continue

        try:
            summary = summarizer(
                text, max_new_tokens=120, min_length=30, do_sample=False
            )[0]["summary_text"]

            article["summary"] = summary

        except Exception:
            pass

        summarized.append(article)

    return summarized
