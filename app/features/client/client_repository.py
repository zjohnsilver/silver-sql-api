from sqlalchemy import text
from sqlalchemy.orm import Session

from app.features.client.client_entity import (
    ClientEntity,
    ConnectionInfoEntity,
)


class ClientRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_all_clients(self) -> list[ClientEntity]:
        sql = text(
            """
            SELECT
                id, name, tag
            FROM manage.client
            WHERE deleted_at IS NULL
            ORDER BY id ASC
            """
        )
        rows = self._db.execute(sql).all()
        clients: list[ClientEntity] = []
        for row in rows:
            row_dict = dict(row._mapping)
            clients.append(
                ClientEntity(
                    id=row_dict["id"],
                    name=row_dict["name"],
                    tag=row_dict["tag"],
                )
            )
        return clients

    def get_connection_info(self, client_id: int) -> ConnectionInfoEntity:
        sql = text(
            """
            SELECT
                con_database
            FROM manage.client
            WHERE id = :client_id
            """
        )
        row = self._db.execute(sql, {"client_id": client_id}).first()
        row_dict = dict(row._mapping)

        con_database = row_dict["con_database"]

        return ConnectionInfoEntity(
            database=con_database["database"],
            username=con_database["user"],
            password=con_database["password"],
            host=con_database["host"],
            port=int(con_database["port"]),
        )
