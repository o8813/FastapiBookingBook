from pymongo import AsyncMongoClient
from config import settings
from pymongo.asynchronous.database import AsyncDatabase

mongo_client: AsyncMongoClient | None = None
mongo_database: AsyncDatabase | None = None

async def connect_db():
    global mongo_client, mongo_database

    mongo_client = AsyncMongoClient(
        settings.mongo_db_url,
        serverSelectionTimeoutMS=5000,
        tz_aware=True
    )

    await mongo_client.admin.command('ping')

    mongo_database = mongo_client[
        settings.mongo_db_name
    ]

async def disconnect_db():
    global mongo_client, mongo_database

    if mongo_client is not None:
        await mongo_client.close()

    mongo_client = None
    mongo_database = None

def get_db():
    if mongo_database is None:
        raise RuntimeError('No connection')
    return mongo_database

def get_collection():
    database = get_db()
    return database['booking']