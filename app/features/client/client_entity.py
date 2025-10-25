from pydantic import BaseModel


class ClientEntity(BaseModel):
    id: int
    name: str
    tag: str | None = None


class ConnectionInfoEntity(BaseModel):
    database: str
    username: str
    password: str
    host: str
    port: int
