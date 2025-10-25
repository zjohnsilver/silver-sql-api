from typing import Optional, List, Any, Literal
from pydantic import BaseModel, Field


class Client(BaseModel):
    id: str
    name: str
    tag: Optional[str] = None


class QueryOptions(BaseModel):
    max_rows: int = Field(default=5000, ge=1, le=100000)
    timeout_seconds: int = Field(default=30, ge=1, le=300)


class ColumnMetadata(BaseModel):
    name: str
    type: str


class QueryResultSelect(BaseModel):
    type: Literal['select'] = 'select'
    columns: List[ColumnMetadata]
    rows: List[List[Any]]
    total_rows: int
    has_more: bool
    next_cursor: Optional[str] = None
    duration_ms: float


class QueryResultNonSelect(BaseModel):
    type: Literal['non_select'] = 'non_select'
    statement_type: str
    rows_affected: int
    duration_ms: float
    messages: Optional[List[str]] = None
    warnings: Optional[List[str]] = None


class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None
    hint: Optional[str] = None

