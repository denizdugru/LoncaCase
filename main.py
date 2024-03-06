from fastapi import FastAPI
from app.endpoints.items import router as items_router
from app.database.mongo_utils import MongoDB

app = FastAPI()

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017"

# Create MongoDB instance
mongo = MongoDB(MONGO_URI)

# Include router
app.include_router(items_router, prefix="/api", tags=["items"])

# Injection of mongo client
app.state.mongo = mongo


# Define shutdown event handler
@app.on_event("shutdown")
async def shutdown_event():
    await mongo.close_connection()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
