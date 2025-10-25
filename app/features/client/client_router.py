from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.features.client.client_schemas import (
    GetAllClientsResponse,
)
from app.features.client.client_service import ClientService
from app.shared.db import get_db

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=GetAllClientsResponse)
async def get_all_clients(
    db: Session = Depends(get_db),
) -> GetAllClientsResponse:
    client_service = ClientService(db)
    clients = client_service.get_all()
    return GetAllClientsResponse(data=clients)
