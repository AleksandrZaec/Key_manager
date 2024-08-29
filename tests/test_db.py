import asyncio
import pytest
from datetime import datetime
from bson import ObjectId

from app.db import save_secret, retrieve_secret, db


@pytest.mark.asyncio
async def test_save_secret():
    """
    Проверяет сохранение секрета в базе данных.
    """
    secret = "test_secret"
    passphrase = "test_passphrase"
    ttl = 60

    secret_key = await save_secret(secret, passphrase, ttl)

    stored_secret = await db.secrets.find_one({"_id": ObjectId(secret_key)})
    assert stored_secret is not None
    assert stored_secret["secret"] == secret
    assert stored_secret["passphrase"] == passphrase
    assert stored_secret["expireAt"] > datetime.utcnow()


@pytest.mark.asyncio
async def test_retrieve_secret():
    """
    Проверяет извлечение секрета из базы данных после истечения времени жизни.
    """
    secret = "test_secret"
    passphrase = "test_passphrase"
    ttl = 60

    secret_key = await save_secret(secret, passphrase, ttl)

    await asyncio.sleep(ttl + 1)

    retrieved_secret = await retrieve_secret(secret_key, passphrase)
    assert retrieved_secret is None

    stored_secret = await db.secrets.find_one({"_id": ObjectId(secret_key)})
    assert stored_secret is None