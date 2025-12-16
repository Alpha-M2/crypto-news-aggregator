from transformers import pipeline

summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", device=0)


def summarize_articles(articles):
    summarized = []
    for article in articles:
        text = article.get("content", "")
        if text:
            summary = summarizer(text, max_new_tokens=150)[0]["summary_text"]
            article["summary"] = summary
            summarized.append(article)
    return summarized
