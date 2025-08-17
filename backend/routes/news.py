from fastapi import APIRouter, HTTPException, status
from typing import List

from services.fetch_news import fetch_and_process_news
from database.mongo import news_collection

router = APIRouter()

@router.post("/fetch-latest-news", status_code=status.HTTP_201_CREATED)
async def fetch_and_store_news():
    try:
        articles = await fetch_and_process_news()
        if not articles:
            return {"message": "No new articles found."}
        
        existing_urls = {doc["url"] async for doc in news_collection.find({}, {"url": 1})}
        new_articles = [article for article in articles if article["url"] not in existing_urls]

        if not new_articles:
            return {"message": "No new articles to store."}
        
        result = await news_collection.insert_many(new_articles)
        return {"message": f"Successfully stored {len(result.inserted_ids)} new articles."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/get-news", response_model=List[dict])
async def get_all_news(skip: int = 0, limit: int = 10):
    news_cursor = news_collection.find().skip(skip).limit(limit)
    news_list = []
    async for news_item in news_cursor:
        news_item["_id"] = str(news_item["_id"])
        news_list.append(news_item)
    return news_list