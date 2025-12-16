# Crypto News Aggregator

A modular Python backend that ingests cryptocurrency news, summarizes content using transformer models, stores results in MongoDB, and exposes them via a REST API.

This project is intentionally built step-by-step to demonstrate real-world backend engineering practices: pipeline design, data processing, persistence, and service delivery.

---

## What This Project Does (Today)

✔ Scrapes multiple crypto news sources (stub-based, extensible)  
✔ Summarizes article text using a lightweight transformer model (`t5-small`)  
✔ Persists summarized articles to MongoDB Atlas  
✔ Exposes stored articles via a Flask REST API  
✔ Uses a clear ingestion → processing → storage → delivery pipeline  
✔ Designed for incremental production hardening  

---

## Architecture Overview

The system is organized as a pipeline with clearly defined responsibilities:

Ingestion → Processing → Storage → Delivery

Each layer is isolated, testable, and replaceable.

---

## Technology Stack

- Python 3.11
- uv (dependency & environment management)
- Requests + BeautifulSoup (scraping)
- Hugging Face Transformers (`t5-small`)
- MongoDB Atlas
- Flask (API delivery)

---

## Setup Instructions

### 1. Environment Setup

```bash
uv venv
source .venv/bin/activate
uv sync
```

### 2. Configuration

Edit config.py and set your MongoDB Atlas connection:

```bash
MONGO_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/"
DB_NAME = "crypto_news"
COLLECTION_NAME = "articles"
```

### 3. Run the Pipeline

This executes ingestion → summarization → storage.

```bash
uv run python run.py
```

### 4. Run the API Server
```bash
uv run python -m app.web
```
Available endpoints:

GET /health – service health check

GET /articles – fetch latest stored articles


### Why This Project Exists

This repository is designed to:

Demonstrate backend and data pipeline engineering skills

Show clean separation of concerns

Be readable, extensible, and production-oriented

Reflect how real systems evolve, not toy scripts
