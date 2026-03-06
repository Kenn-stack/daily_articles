import asyncio
from telegram.error import TimedOut
from utils import send_article, get_article

async def main():
    articles = get_article()
    for article in articles:
        #retry logic to handle potential timeouts when sending messages
        for _ in range(3):
            try:
                image = article.media_content[0]['url'] if 'media_content' in article else None
                await send_article(article.title, article.link, article.description, image)
                break  # Break out of the retry loop if successful
            except TimedOut:
                await asyncio.sleep(3)

        else:
            print("Failed to send message for article:", article.title)



if __name__ == "__main__":
   asyncio.run(main())
