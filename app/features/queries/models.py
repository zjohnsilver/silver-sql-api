from typing import Optional
from pydantic import BaseModel
from app.shared.models import QueryOptions


class QueryExecuteRequest(BaseModel):
    client_id: str
    sql: str
    options: Optional[QueryOptions] = None

