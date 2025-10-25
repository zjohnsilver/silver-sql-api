from typing import List
from fastapi import APIRouter, Query, HTTPException
from app.shared.models import Client
from app.features.clients.models import ConnectionResolveResponse
from app.features.clients.service import client_service

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=List[Client])
async def search_clients(
    search: str = Query("", description="Search term for client name or tag"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
):
    """
    Search for clients by name or tag.
    """
    clients = await client_service.search_clients(search, limit)
    return clients


@router.post("/{client_id}/resolve", response_model=ConnectionResolveResponse)
async def resolve_connection(client_id: str):
    """
    Verify that connection information is available for a client.
    """
    result = await client_service.resolve_connection(client_id)
    
    if result["status"] == "failed":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result

