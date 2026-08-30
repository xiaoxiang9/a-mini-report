from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.config.settings import get_settings


engine = create_engine(get_settings().database_url, pool_pre_ping=True)
SessionFactory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
