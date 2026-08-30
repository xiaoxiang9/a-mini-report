from collections.abc import Callable

from fastapi import FastAPI

from app.application.home.get_home_summary import GetHomeSummary
from app.infrastructure.database.health import check_database
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.platform.sqlalchemy_repository import SqlAlchemyHomeSummaryRepository
from app.interfaces.http.routes.health import build_health_router
from app.interfaces.http.routes.home import build_home_router


def create_app(
    home_use_case: GetHomeSummary | None = None,
    database_checker: Callable[[], str] | None = None,
) -> FastAPI:
    app = FastAPI(title="A股投资策略平台 API", version="0.1.0")
    if home_use_case is None:
        session = SessionFactory()
        home_use_case = GetHomeSummary(SqlAlchemyHomeSummaryRepository(session))
    if database_checker is None:
        def database_checker() -> str:
            session = SessionFactory()
            try:
                return check_database(session)
            finally:
                session.close()

    app.include_router(build_health_router(database_checker), prefix="/api")
    app.include_router(build_home_router(home_use_case), prefix="/api")
    return app
