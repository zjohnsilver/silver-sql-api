from typing import Union
from fastapi import APIRouter, HTTPException
from app.shared.models import QueryResultSelect, QueryResultNonSelect
from app.features.queries.models import QueryExecuteRequest
from app.features.queries.service import query_service

router = APIRouter(prefix="/query", tags=["queries"])


@router.post("/execute", response_model=Union[QueryResultSelect, QueryResultNonSelect])
async def execute_query(request: QueryExecuteRequest):
    """
    Execute a SQL query against a client's database.
    
    - **client_id**: ID of the client/database to query
    - **sql**: SQL statement to execute
    - **options**: Optional execution parameters (max_rows, timeout_seconds)
    """
    options = request.options or {}
    max_rows = options.max_rows if hasattr(options, 'max_rows') else 5000
    timeout_seconds = options.timeout_seconds if hasattr(options, 'timeout_seconds') else 30
    
    result = await query_service.execute_query(
        client_id=request.client_id,
        sql=request.sql,
        max_rows=max_rows,
        timeout_seconds=timeout_seconds
    )
    return result


@router.post("/{query_id}/cancel")
async def cancel_query(query_id: str):
    """
    Cancel a running query.
    
    Note: Implementation requires query tracking and cancellation support.
    """
    # TODO: Implement query cancellation
    raise HTTPException(
        status_code=501,
        detail="Query cancellation not yet implemented"
    )

