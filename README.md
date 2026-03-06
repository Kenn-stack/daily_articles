# Telegram RSS Article Bot

A simple Python bot that fetches articles from RSS feeds and sends them to your Telegram daily.

---

## Features

* Sends article title, description, published date, and link
* Supports images if available
* Description in italic and blockquote, title and published date in bold
* Uses SQLite to avoid duplicate articles
* Retry logic for Telegram timeouts

---

## Requirements

* Python 3.13+
* `python-telegram-bot`, `feedparser`, `beautifulsoup4`


## Run

```bash
uv run main.py
```


