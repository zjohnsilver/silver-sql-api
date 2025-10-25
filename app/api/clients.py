from typing import List
from fastapi import APIRouter, Query, HTTPException, Depends
from app.models.schemas import Client, ConnectionResolveResponse
from app.services.client_service import client_service
from app.core.auth import get_current_user

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=List[Client])
async def search_clients(
    search: str = Query("", description="Search term for client name or tag"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    user: dict = Depends(get_current_user)
):
    """
    Search for clients by name or tag.
    """
    clients = await client_service.search_clients(search, limit)
    return clients


@router.post("/{client_id}/resolve", response_model=ConnectionResolveResponse)
async def resolve_connection(
    client_id: str,
    user: dict = Depends(get_current_user)
):
    """
    Verify that connection information is available for a client.
    """
    result = await client_service.resolve_connection(client_id)
    
    if result["status"] == "failed":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result

