from collections.abc import Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.home.get_home_summary import GetHomeSummary
from app.infrastructure.database.health import check_database
from app.infrastructure.database.session import SessionFactory
from app.infrastructure.config.settings import get_settings
from app.infrastructure.platform.sqlalchemy_repository import SqlAlchemyHomeSummaryRepository
from app.infrastructure.stock_tracking.sqlalchemy_repository import SqlAlchemyStockTrackingRepository
from app.infrastructure.stock_tracking.tushare_provider import TushareStockDataProvider
from app.application.stock_tracking.add_tracked_stock import AddTrackedStock
from app.application.stock_tracking.get_stock_detail import GetStockDetail
from app.application.stock_tracking.list_tracked_stocks import ListTrackedStocks
from app.application.stock_tracking.remove_tracked_stock import RemoveTrackedStock
from app.application.stock_tracking.sync_tracked_stocks import SyncTrackedStocks
from app.domain.stock_tracking.providers import StockDataProvider
from app.domain.stock_tracking.repositories import StockTrackingRepository
from app.interfaces.http.routes.health import build_health_router
from app.interfaces.http.routes.home import build_home_router
from app.interfaces.http.routes.stocks import build_stocks_router


def create_app(
    home_use_case: GetHomeSummary | None = None,
    database_checker: Callable[[], str] | None = None,
    stock_repository: StockTrackingRepository | None = None,
    stock_provider: StockDataProvider | None = None,
) -> FastAPI:
    app = FastAPI(title="A股投资策略平台 API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "https://myxiang.online",
            "https://www.myxiang.online",
        ],
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
    )
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
    if stock_repository is None:
        stock_repository = SqlAlchemyStockTrackingRepository(SessionFactory())
    if stock_provider is None:
        try:
            stock_provider = TushareStockDataProvider(get_settings().tushare_token)
        except RuntimeError as error:
            provider_error = error

            class UnavailableStockProvider:
                def fetch_snapshot(self, ts_code: str, history: tuple[dict[str, object], ...]):
                    raise provider_error

            stock_provider = UnavailableStockProvider()
    app.include_router(build_stocks_router(
        ListTrackedStocks(stock_repository), GetStockDetail(stock_repository),
        AddTrackedStock(stock_repository, stock_provider), RemoveTrackedStock(stock_repository),
        SyncTrackedStocks(stock_repository, stock_provider),
    ), prefix="/api")
    return app
