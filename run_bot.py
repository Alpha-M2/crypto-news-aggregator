import os
import logging
import asyncio

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from app.bot.telegram_bot import start, stop, delivery_loop


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - telegram_bot - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting Telegram bot...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    async def post_init(application):
        await application.bot.initialize()
        application.create_task(delivery_loop(application.bot))

        logger.info("Delivery loop started")

    app.post_init = post_init

    logger.info("Bot is running and polling for updates")
    app.run_polling()


if __name__ == "__main__":
    main()
