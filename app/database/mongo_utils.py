from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database


class MongoDB:
    def __init__(self, uri: str) -> None:
        self.client = AsyncIOMotorClient(uri)

    async def close_connection(self) -> None:
        self.client.close()
