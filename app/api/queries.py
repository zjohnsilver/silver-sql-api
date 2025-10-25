from typing import Union
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import (
    QueryExecuteRequest,
    QueryResultSelect,
    QueryResultNonSelect,
)
from app.services.query_service import query_service
from app.core.auth import get_current_user

router = APIRouter(prefix="/query", tags=["queries"])


@router.post("/execute", response_model=Union[QueryResultSelect, QueryResultNonSelect])
async def execute_query(
    request: QueryExecuteRequest,
    user: dict = Depends(get_current_user)
):
    """
    Execute a SQL query against a client's database.
    
    - **client_id**: ID of the client/database to query
    - **sql**: SQL statement to execute
    - **options**: Optional execution parameters (max_rows, timeout_seconds)
    """
    result = await query_service.execute_query(request, user)
    return result


@router.post("/{query_id}/cancel")
async def cancel_query(
    query_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Cancel a running query.
    
    Note: Implementation requires query tracking and cancellation support.
    """
    # TODO: Implement query cancellation
    raise HTTPException(
        status_code=501,
        detail="Query cancellation not yet implemented"
    )

