from app.configs.config import InternalConfig

from fastapi import FastAPI
from app.endpoints.items import router as items_router
from mongoengine import connect

app = FastAPI()

# MongoDB connection settings
MONGO_URI = f"mongodb://{InternalConfig.MONGO_HOST}:27017/test"

# Create MongoDB instance
connect(host=MONGO_URI)

# Include router
app.include_router(items_router, prefix="/api", tags=["items"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
