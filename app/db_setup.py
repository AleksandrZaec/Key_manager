import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongodb:27017")
db = client.secret_db


async def create_ttl_index():
    """
    Создание TTL индекса на поле 'expireAt' для автоматического удаления документов по истечении времени.
    """
    await db.secrets.create_index(
        [("expireAt", 1)],
        expireAfterSeconds=0
    )
    print("TTL индекс создан на поле 'expireAt'.")


async def initialize_db():
    await create_ttl_index()
