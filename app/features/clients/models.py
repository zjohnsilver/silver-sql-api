from typing import Optional
from pydantic import BaseModel


class ConnectionResolveResponse(BaseModel):
    status: str
    message: Optional[str] = None

