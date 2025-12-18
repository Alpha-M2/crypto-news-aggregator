## Crypto News Aggregator with Telegram Bot (BlockoraBot)

A production-grade crypto news aggregation pipeline that collects, normalizes, deduplicates, summarizes, and delivers real-time crypto news directly to Telegram subscribers.

**Live Bot:** @BlockoraBot
**Tech Stack:** Python, MongoDB, RSS, Web Scraping, AsyncIO, Telegram Bot API

---

## Overview

This project continuously aggregates crypto news from multiple sources (RSS feeds and scraped sites), processes the data through a robust pipeline, and delivers clean, readable summaries to Telegram users on demand.

Users interact via Telegram commands:

* `/start` — begin receiving crypto news
* `/stop` — stop delivery at any time

Delivery is **stateful per user**, ensuring:

* No duplicate articles
* Independent delivery timelines per subscriber
* Safe restarts with accurate resume points

---

## Key Features

### News Aggregation

* RSS ingestion from major crypto outlets
* Web scraping fallback for poorly structured feeds
* Normalized article schema across sources

### Data Processing Pipeline

* Deterministic article IDs for deduplication
* MongoDB-backed persistence
* UTC-based timestamps for consistent ordering
* Clean HTML stripping using BeautifulSoup

### Telegram Bot Integration

* Multi-subscriber support
* `/start` and `/stop` command handling
* Background async delivery loop
* Per-user `last_delivered_at` tracking
* Clean, readable message formatting

### Reliability & Safety

* Duplicate-safe inserts
* HTML sanitization
* Robust async error handling
* Non-blocking Telegram polling

---

## Requirements

* Python 3.10+
* MongoDB (local or cloud)
* Telegram Bot Token
* `uv` package manager

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Alpha-M2/crypto-news-aggregator.git
cd crypto-news-aggregator
```

### 2. Create Virtual Environment

```bash
uv venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
uv sync
```

### 4. Environment Variables

Create a `.env` file:

```env
MONGO_URI=mongodb://localhost:27017
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

---

## Running the Pipeline (News Ingestion)

Fetches, processes, and stores news articles:

```bash
uv run python run.py
```

This can be scheduled using cron or a job runner.

---

## Running the Telegram Bot

Starts the Telegram bot and delivery loop:

```bash
uv run python run_bot.py
```

Then on Telegram:

1. Search for **@BlockoraBot**
2. Send `/start` to subscribe
3. Send `/stop` to unsubscribe

---

## How Delivery Works

* Each subscriber is stored in MongoDB
* `last_delivered_at` is updated after each successful send
* On restart, delivery resumes safely
* Duplicate messages are prevented by design

---

## Deployment Notes

To run 24/7, the bot must be deployed to an always-on server (VPS or cloud service). Local execution will stop when the terminal closes.

Recommended:

* VPS (DigitalOcean, Hetzner, AWS EC2)
* `systemd` or Docker for process management

---

## Future Improvements

* Per-coin subscriptions
* Inline pause/resume buttons
* Message batching and rate limiting
* Dockerized deployment
* Monitoring and alerting

---

## License

MIT License

---

## Author

Built by **Alpha_M2**
Backend-focused engineer with emphasis on async systems and production-ready Python.
