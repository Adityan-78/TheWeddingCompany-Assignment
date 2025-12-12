import motor.motor_asyncio
from app.config import settings

_client = None

def get_client():
    global _client
    if _client is None:
        _client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    return _client

def get_master_db():
    return get_client()[settings.MASTER_DB]
