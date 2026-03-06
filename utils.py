import os
import sqlite3
from telegram import Bot
import feedparser
import random
from bs4 import BeautifulSoup


urls = ['https://www.thecollector.com/ancient-history/rss/',
        'https://www.thecollector.com/medieval-history/rss/',
        'https://www.thecollector.com/european-history/rss/',
        'https://www.thecollector.com/world-history/rss/',
        'https://www.thecollector.com/military-history/rss/',
        'https://www.thecollector.com/answers/rss/']

#Telegram Bot credentials
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

#SQLite database setup
conn = sqlite3.connect("articles.db")
cursor = conn.cursor()


def create_table():
    """ Create the sent_articles table if it doesn't exist."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sent_articles (
        link TEXT PRIMARY KEY
    )
    """)

    conn.commit()


def clean_html(html_text):
    """
    Clean HTML tags from the description using BeautifulSoup and return plain text.
    """
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text()
    return text.strip()


async def send_article(title, link, description, image=None):
    """
    Send an article to the Telegram channel.
    """
    clean_description = clean_html(description)
    message = f"""
<b>📚 {title}</b>

<blockquote><i>{clean_description[:400]}</i></blockquote>

Read here: {link}
"""
    # await bot.send_message(chat_id=CHAT_ID, text=message)
    if image:
        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=image,
            caption=message,
            parse_mode="HTML",        
        )
    else:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

def already_sent(link):
    """
    Check if an article has already been sent.
    """
    create_table()
    cursor.execute(
        "SELECT 1 FROM sent_articles WHERE link=?",
        (link,)
    )
    return cursor.fetchone() is not None


def mark_as_sent(link):
    """
    Mark an article as sent by adding its link to the database.
    """
    create_table()
    cursor.execute(
        "INSERT OR IGNORE INTO sent_articles VALUES (?)",
        (link,)
    )
    conn.commit()


def get_article():
    """
    Fetch articles from the RSS feeds and return a list of articles that haven't been sent yet.
    """
    feed_urls = random.sample(urls, 2)
    articles = []
    for feed_url in feed_urls:
        feed = feedparser.parse(feed_url)
        available = []

        for entry in feed.entries:
            if not already_sent(entry.link):
                available.append(entry)

        article = random.choice(available)

        mark_as_sent(article.link)
        articles.append(article)

    return articles
