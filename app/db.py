import motor.motor_asyncio
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import pytz

moscow_tz = pytz.timezone('Europe/Moscow')

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongodb:27017")
db = client.secret_db


async def save_secret(encrypted_secret: str, passphrase: str, ttl: int) -> str:
    """
    Асинхронное сохранение зашифрованного секрета в базу данных с указанием кодовой фразы и времени жизни.
    Возвращает уникальный идентификатор секрета.
    """
    expire_at = datetime.now(moscow_tz) + timedelta(seconds=ttl)
    secret_document = {
        "secret": encrypted_secret,
        "expireAt": expire_at,
        "passphrase": passphrase
    }
    secret = await db.secrets.insert_one(secret_document)
    return str(secret.inserted_id)


async def retrieve_secret(secret_key: str, passphrase: str) -> str:
    """
    Асинхронное получение и удаление секрета по его ключу и кодовой фразе.
    Возвращает зашифрованный секрет или None, если секрет не найден или кодовая фраза неверна.
    """
    secret = await db.secrets.find_one_and_delete({
        "_id": ObjectId(secret_key),
        "passphrase": passphrase,
        "expireAt": {"$gt": datetime.now(moscow_tz)}
    })
    if secret:
        return secret["secret"]
    return None
