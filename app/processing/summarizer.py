from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small", device=0)


def summarize_articles(articles):
    texts_to_summarize = []
    indices_to_summarize = []

    # First pass: identify articles needing summarization
    for i, article in enumerate(articles):
        text = article.get("summary") or article.get("title", "")

        if len(text.split()) >= 30:
            texts_to_summarize.append(text)
            indices_to_summarize.append(i)

    # Batch process all qualifying texts at once if any exist
    if texts_to_summarize:
        try:
            logger.info(f"Batch summarizing {len(texts_to_summarize)} articles...")
            summaries = summarizer(
                texts_to_summarize, 
                max_new_tokens=120, 
                min_length=30, 
                do_sample=False,
                batch_size=8
            )
            
            # Map summaries back to original articles
            for j, result in enumerate(summaries):
                original_idx = indices_to_summarize[j]
                articles[original_idx]["summary"] = result["summary_text"]
                
        except Exception as e:
            logger.error(f"Failed batch summarization: {e}")

    return articles
