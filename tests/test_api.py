import pytest
from httpx import AsyncClient
from app.main import app

client = AsyncClient(app=app, base_url="http://test")

@pytest.mark.asyncio
async def test_generate_secret():
    """
    Проверяет создание нового секрета и возврат уникального идентификатора.
    """
    response = await client.post("/generate", json={
        "secret": "test_secret",
        "passphrase": "test_passphrase",
        "ttl": 60
    })
    assert response.status_code == 200
    response_json = response.json()
    assert "secret_key" in response_json

@pytest.mark.asyncio
async def test_get_secret():
    """
    Проверяет извлечение секрета по ключу и правильной кодовой фразе.
    """
    response = await client.post("/generate", json={
        "secret": "test_secret",
        "passphrase": "test_passphrase",
        "ttl": 60
    })
    assert response.status_code == 200
    response_json = response.json()
    secret_key = response_json["secret_key"]

    response = await client.post(f"/secrets/{secret_key}", json={
        "passphrase": "test_passphrase"
    })
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["secret"] == "test_secret"

@pytest.mark.asyncio
async def test_get_secret_invalid_passphrase():
    """
    Проверяет попытку извлечения секрета с неверной кодовой фразой.
    """
    response = await client.post("/generate", json={
        "secret": "test_secret",
        "passphrase": "test_passphrase",
        "ttl": 60
    })
    assert response.status_code == 200
    response_json = response.json()
    secret_key = response_json["secret_key"]

    response = await client.post(f"/secrets/{secret_key}", json={
        "passphrase": "wrong_passphrase"
    })
    assert response.status_code == 404