import os
import httpx
from datetime import datetime

#API_KEY = os.getenv("GNEWS_API_KEY")
API_KEY = "86130dd949884799ab00599db9e72f58"
BASE_URL = "https://gnews.io/api/v4/top-headlines"

async def fetch_and_process_news():
    if not API_KEY:
        raise ValueError("GNEWS_API_KEY is not set in environment variables.")
    
    params = {
        "token": API_KEY,
        "lang": "en",
        "country": "in",
        "max": 10
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            news_data = response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return []
        
        processed_articles = []
        for article in news_data.get("articles", []):
            processed_articles.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content"),
                "url": article.get("url"),
                "published_at": datetime.strptime(article.get("publishedAt"), "%Y-%m-%dT%H:%M:%SZ") if article.get("publishedAt") else None,
                "source": article.get("source", {}).get("name")
            })
        
        return processed_articles