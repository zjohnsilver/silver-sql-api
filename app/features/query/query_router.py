from typing import Union

from fastapi import APIRouter, Body, Depends, Header
from sqlalchemy.orm import Session

from app.features.client.client_service import ClientService
from app.features.query.query_service import QueryService
from app.shared.db import create_engine_from_connection_info, get_db
from app.shared.models import QueryResultNonSelect, QueryResultSelect

router = APIRouter(prefix="/queries", tags=["queries"])


@router.post(
    "/execute", response_model=Union[QueryResultSelect, QueryResultNonSelect]
)
async def execute_query(
    body: str = Body(..., media_type="text/plain"),
    client_id: int = Header(...),
    db: Session = Depends(get_db),
) -> Union[QueryResultSelect, QueryResultNonSelect]:
    client_service = ClientService(db)
    connection_info = client_service.get_connection_info(client_id)
    engine = create_engine_from_connection_info(connection_info)
    query_service = QueryService()
    return query_service.execute(engine, body)
