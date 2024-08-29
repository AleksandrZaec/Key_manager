from fastapi import APIRouter, HTTPException
from app.models import SecretCreateRequest, SecretRetrieveRequest
from app.db import save_secret, retrieve_secret

router = APIRouter()


@router.post("/generate")
async def generate_secret(request: SecretCreateRequest):
    """
    Создает новый секрет и возвращает уникальный идентификатор.
    """
    secret_key = await save_secret(request.secret, request.passphrase, request.ttl)
    return {"secret_key": secret_key}


@router.post("/secrets/{secret_key}")
async def get_secret(secret_key: str, request: SecretRetrieveRequest):
    """
    Получает секрет по его ключу и кодовой фразе.
    """
    secret = await retrieve_secret(secret_key, request.passphrase)
    if secret:
        return {"secret": secret}
    else:
        raise HTTPException(status_code=404, detail="Секрет удален или кодовое слово неверное")
