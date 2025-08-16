from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["TruthLens"]

news_collection = db["news"]

async def check_connection():
    try:
        await client.server_info()
        print("MongoDB connection is successful.")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_connection())