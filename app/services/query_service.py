import time
import re
import asyncio
from typing import Union, List, Any, Tuple
from fastapi import HTTPException
from app.models.schemas import (
    QueryExecuteRequest,
    QueryResultSelect,
    QueryResultNonSelect,
    ColumnMetadata,
)
from app.services.client_service import client_service


class QueryService:
    """
    Service for executing SQL queries against client databases.
    """
    
    def _parse_statement_type(self, sql: str) -> str:
        """
        Determine the type of SQL statement.
        """
        sql_stripped = sql.strip().upper()
        
        if sql_stripped.startswith('SELECT'):
            return 'SELECT'
        elif sql_stripped.startswith('INSERT'):
            return 'INSERT'
        elif sql_stripped.startswith('UPDATE'):
            return 'UPDATE'
        elif sql_stripped.startswith('DELETE'):
            return 'DELETE'
        elif sql_stripped.startswith('CREATE'):
            return 'CREATE'
        elif sql_stripped.startswith('DROP'):
            return 'DROP'
        elif sql_stripped.startswith('ALTER'):
            return 'ALTER'
        else:
            return 'UNKNOWN'
    
    def _validate_sql(self, sql: str) -> None:
        """
        Basic SQL validation and security checks.
        """
        # Check for multiple statements (no semicolons except at end)
        sql_stripped = sql.strip().rstrip(';')
        if ';' in sql_stripped:
            raise HTTPException(
                status_code=400,
                detail="Multiple statements not allowed"
            )
        
        # Check for dangerous patterns (basic protection)
        dangerous_patterns = [
            r'\bDROP\s+DATABASE\b',
            r'\bDROP\s+SCHEMA\b',
            r'\bTRUNCATE\b',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, sql, re.IGNORECASE):
                raise HTTPException(
                    status_code=403,
                    detail=f"Statement contains forbidden operation: {pattern}"
                )
    
    def _check_policy(self, statement_type: str, user_roles: List[str]) -> None:
        """
        Check if user has permission to execute this statement type.
        """
        # Example policy: only SELECT allowed for read-only roles
        if 'read_only' in user_roles and statement_type != 'SELECT':
            raise HTTPException(
                status_code=403,
                detail=f"Your role does not permit {statement_type} statements"
            )
    
    async def _execute_on_connection(
        self,
        conn_info: dict,
        sql: str,
        max_rows: int,
        timeout_seconds: int
    ) -> Tuple[List[ColumnMetadata], List[List[Any]], int, str]:
        """
        Execute SQL on the target database connection.
        
        In production, this would use actual database drivers (asyncpg, aiomysql, etc.)
        based on conn_info['driver'].
        
        Returns: (columns, rows, rows_affected, statement_type)
        """
        # Mock implementation - replace with actual DB execution
        statement_type = self._parse_statement_type(sql)
        
        # Simulate execution time
        await asyncio.sleep(0.1)
        
        if statement_type == 'SELECT':
            # Mock SELECT result
            columns = [
                ColumnMetadata(name="id", type="integer"),
                ColumnMetadata(name="name", type="varchar"),
                ColumnMetadata(name="value", type="numeric"),
            ]
            rows = [
                [1, "Sample Row 1", 100.50],
                [2, "Sample Row 2", 200.75],
                [3, "Sample Row 3", 300.25],
            ]
            return columns, rows, len(rows), statement_type
        else:
            # Mock non-SELECT result
            return [], [], 5, statement_type  # 5 rows affected
    
    async def execute_query(
        self,
        request: QueryExecuteRequest,
        user: dict
    ) -> Union[QueryResultSelect, QueryResultNonSelect]:
        """
        Main query execution method.
        """
        start_time = time.time()
        
        # Get connection info
        conn_info = await client_service.get_connection_info(request.client_id)
        if not conn_info:
            raise HTTPException(
                status_code=404,
                detail=f"Client {request.client_id} not found"
            )
        
        # Validate SQL
        self._validate_sql(request.sql)
        
        # Parse statement type
        statement_type = self._parse_statement_type(request.sql)
        
        # Check policy
        user_roles = user.get('roles', [])
        self._check_policy(statement_type, user_roles)
        
        # Get options
        options = request.options or {}
        max_rows = options.max_rows if hasattr(options, 'max_rows') else 5000
        timeout_seconds = options.timeout_seconds if hasattr(options, 'timeout_seconds') else 30
        
        # Execute query
        try:
            columns, rows, rows_affected, stmt_type = await asyncio.wait_for(
                self._execute_on_connection(conn_info, request.sql, max_rows, timeout_seconds),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=408,
                detail=f"Query execution exceeded timeout of {timeout_seconds}s"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Query execution failed: {str(e)}"
            )
        
        duration_ms = (time.time() - start_time) * 1000
        
        # Build response based on statement type
        if stmt_type == 'SELECT':
            has_more = len(rows) >= max_rows
            return QueryResultSelect(
                columns=columns,
                rows=rows,
                total_rows=len(rows),
                has_more=has_more,
                duration_ms=duration_ms
            )
        else:
            return QueryResultNonSelect(
                statement_type=stmt_type,
                rows_affected=rows_affected,
                duration_ms=duration_ms,
                messages=[f"{stmt_type} completed successfully"]
            )


query_service = QueryService()

