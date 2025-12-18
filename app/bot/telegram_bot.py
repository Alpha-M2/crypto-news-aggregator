import time
import asyncio
from datetime import datetime, timezone

from telegram import Bot, Update
from app.config import TELEGRAM_BOT_TOKEN

from app.storage.subscriptions import (
    activate_subscription,
    deactivate_subscription,
    get_active_subscriptions,
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


async def delivery_loop(bot: Bot):
    while True:
        subscriptions = get_active_subscriptions()

        for sub in subscriptions:
            last = sub.get("last_delivered_at") or datetime(
                1970, 1, 1, tzinfo=timezone.utc
            )

            articles = fetch_undelivered_articles(last)

            for article in articles:
                message = (
                    f"*{article['title']}*\n\n{article['summary']}\n\n{article['url']}"
                )

                await bot.send_message(
                    chat_id=sub["chat_id"],
                    text=message,
                    parse_mode="Markdown",
                )

                sub["last_delivered_at"] = article["created_at"]

        await asyncio.sleep(30)
