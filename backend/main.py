from fastapi import FastAPI
from routes.news import router as news_router
from database.mongo import connect_to_mongo

app = FastAPI(title="News Verifier API")

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

app.include_router(news_router, prefix="/api", tags=["News"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Verifier API"}