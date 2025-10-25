from typing import List, Optional
from app.shared.models import Client


class ClientService:
    """
    Service for managing client connections and metadata.
    In production, this would query the client-management database.
    """
    
    # Mock data for development
    _mock_clients = [
        Client(id="client-1", name="Production Database", tag="prod"),
        Client(id="client-2", name="Staging Database", tag="staging"),
        Client(id="client-3", name="Analytics Warehouse", tag="analytics"),
        Client(id="client-4", name="Development DB", tag="dev"),
        Client(id="client-5", name="Customer Reports", tag="reporting"),
    ]
    
    async def search_clients(self, search: str, limit: int = 20) -> List[Client]:
        """
        Search for clients by name or tag.
        """
        if not search:
            return self._mock_clients[:limit]
        
        search_lower = search.lower()
        filtered = [
            client for client in self._mock_clients
            if search_lower in client.name.lower() or 
               (client.tag and search_lower in client.tag.lower())
        ]
        
        return filtered[:limit]
    
    async def get_client_by_id(self, client_id: str) -> Optional[Client]:
        """
        Get a specific client by ID.
        """
        for client in self._mock_clients:
            if client.id == client_id:
                return client
        return None
    
    async def get_connection_info(self, client_id: str) -> Optional[dict]:
        """
        Get database connection information for a client.
        In production, this would fetch from the client-management DB.
        
        Returns connection dict with: host, port, database, user, password, driver
        """
        client = await self.get_client_by_id(client_id)
        if not client:
            return None
        
        # Mock connection info - replace with actual DB lookup
        return {
            "driver": "postgresql",  # or "mysql", "mssql", etc.
            "host": "localhost",
            "port": 5432,
            "database": f"db_{client_id}",
            "user": "sql_user",
            "password": "sql_password",
        }
    
    async def resolve_connection(self, client_id: str) -> dict:
        """
        Verify that connection info is available and valid.
        """
        conn_info = await self.get_connection_info(client_id)
        if not conn_info:
            return {
                "status": "failed",
                "message": f"Client {client_id} not found"
            }
        
        # In production, you might want to test the connection here
        return {
            "status": "resolved",
            "message": f"Connected to {conn_info['database']}"
        }


client_service = ClientService()

