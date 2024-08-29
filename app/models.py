from pydantic import BaseModel, Field, constr


class SecretCreateRequest(BaseModel):
    """
    Модель данных для создания нового секрета.
    """
    secret: constr(min_length=1)
    passphrase: constr(min_length=1)
    ttl: int = Field(gt=0, le=3600)


class SecretRetrieveRequest(BaseModel):
    """
    Модель данных для получения секрета.
    """
    passphrase: constr(min_length=1)
