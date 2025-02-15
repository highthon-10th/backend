from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import ssl

client = None
db = None

async def init_db():
    global client, db
    client = AsyncIOMotorClient(
        settings.MONGODB_URL,
        tls=True,
        tlsInsecure=False,  # Set to True only for testing if needed
        serverSelectionTimeoutMS=5000,
    )
    db = client[settings.DATABASE_NAME]
    
async def close_db():
    if client is not None:
        client.close()

def get_db():
    return db