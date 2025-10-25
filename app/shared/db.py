import threading
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.features.client.client_entity import ConnectionInfoEntity
from app.shared.config import settings

engine = create_engine(settings.DATABASE_URL, future=True)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_engine_from_connection_info(info: ConnectionInfoEntity) -> Engine:
    url = f"postgresql+psycopg2://{info.username}:{info.password}@{info.host}:{info.port}/{info.database}"
    return create_engine(url, future=True)


def execute_with_timeout(engine: Engine, sql: str, timeout_seconds: int = 30):
    cancelled = False

    def do_cancel():
        nonlocal cancelled
        cancelled = True
        try:
            raw = conn.connection
            raw.cancel()
        except Exception:
            pass

    with engine.connect() as conn:
        timer = threading.Timer(timeout_seconds, do_cancel)
        timer.start()
        try:
            result = conn.execute(sql)
            if result.returns_rows:
                rows = result.fetchall()
                keys = list(result.keys())
                return keys, [list(r) for r in rows], len(rows)
            return [], [], result.rowcount
        except Exception as e:
            if cancelled:
                raise TimeoutError("query_timeout")
            raise e
        finally:
            try:
                timer.cancel()
            except Exception as e:
                raise Exception(f"Error canceling timer: {e}")
