from pydantic import BaseModel

from app.features.client.client_entity import ClientEntity


class GetAllClientsResponse(BaseModel):
    data: list[ClientEntity]
