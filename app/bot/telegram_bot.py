import asyncio

import re
import html

from datetime import datetime, timezone
from telegram import Bot, Update
from bs4 import BeautifulSoup

from app.storage.subscriptions import (
    activate_subscription,
    deactivate_subscription,
    update_last_delivered,
    get_active_subscriptions_with_last_delivered,
)
from app.storage.mongodb import fetch_undelivered_articles


async def start(update: Update, context):
    chat_id = update.effective_chat.id
    activate_subscription(chat_id)
    await update.message.reply_text("Crypto news delivery started.")


async def stop(update: Update, context):
    chat_id = update.effective_chat.id
    deactivate_subscription(chat_id)
    await update.message.reply_text("Crypto news delivery stopped.")


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Decode HTML entities and strip tags
    text = html.unescape(text)
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text


async def delivery_loop(bot: Bot):
    print("Delivery loop started")

    while True:
        try:
            subscriptions = get_active_subscriptions_with_last_delivered()

            for sub in subscriptions:
                last_delivered = sub.get("last_delivered_at") or datetime(
                    1970, 1, 1, tzinfo=timezone.utc
                )

                articles = fetch_undelivered_articles(last_delivered)

                for article in articles:
                    title = clean_text(article.get("title", ""))
                    summary = clean_text(article.get("summary", ""))
                    message = f"<b>{title}</b>\n\n{summary}\n\n{article['url']}"

                    try:
                        await bot.send_message(
                            chat_id=sub["chat_id"],
                            text=message,
                            parse_mode="HTML",
                            disable_web_page_preview=True,
                        )

                        update_last_delivered(sub["chat_id"], article["created_at"])

                    except Exception as e:
                        print(f"Failed to send article to {sub['chat_id']}: {e}")
                        continue

        except Exception as e:
            print(f"Delivery loop error: {e}")

        await asyncio.sleep(30)
