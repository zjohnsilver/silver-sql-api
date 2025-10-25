from sqlalchemy.orm import Session

from app.features.client.client_entity import (
    ClientEntity,
    ConnectionInfoEntity,
)
from app.features.client.client_repository import ClientRepository


class ClientService:
    def __init__(self, db: Session):
        self._db = db
        self._client_repository = ClientRepository(db)

    def get_all(self) -> list[ClientEntity]:
        return self._client_repository.get_all_clients()

    def get_connection_info(self, client_id: int) -> ConnectionInfoEntity:
        return self._client_repository.get_connection_info(client_id)
