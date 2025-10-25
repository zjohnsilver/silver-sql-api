import time
from typing import Union

from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.shared.db import execute_with_timeout
from app.shared.models import (
    ColumnMetadata,
    QueryResultNonSelect,
    QueryResultSelect,
)


class QueryService:
    def execute(
        self, engine: Engine, sql: str
    ) -> Union[QueryResultSelect, QueryResultNonSelect]:
        started = time.time()
        stmt = sql.strip()
        is_select = stmt.upper().startswith("SELECT")
        keys, rows, count = execute_with_timeout(engine, text(stmt), 30)
        duration_ms = (time.time() - started) * 1000
        if is_select:
            columns = [ColumnMetadata(name=k, type="unknown") for k in keys]
            return QueryResultSelect(
                columns=columns,
                rows=rows,
                total_rows=len(rows),
                has_more=False,
                duration_ms=duration_ms,
            )
        return QueryResultNonSelect(
            statement_type="NON_SELECT",
            rows_affected=count,
            duration_ms=duration_ms,
        )
