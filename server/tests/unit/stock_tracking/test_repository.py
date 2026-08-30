import json

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.domain.stock_tracking.models import StockDetail
from app.infrastructure.stock_tracking.sqlalchemy_repository import SqlAlchemyStockTrackingRepository


def test_repository_saves_and_lists_only_tracked_stocks() -> None:
    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE StockDetail (
                tsCode TEXT PRIMARY KEY, stockName TEXT, exchange TEXT, isTracked BOOLEAN,
                currentPrice FLOAT, change7dPercent FLOAT, peTtm FLOAT, pePercentile FLOAT,
                pb FLOAT, pbPercentile FLOAT, valuationHistoryJson TEXT, latestTradeDate DATE,
                dataSource TEXT, lastSyncedAt DATETIME, syncError TEXT
            )
        """))

    with Session(engine) as session:
        repository = SqlAlchemyStockTrackingRepository(session)
        repository.save(StockDetail(
            "600519.SH", "贵州茅台", "SH", True, 1500, 2.5, 30, 60, 8, 55,
            ({"trade_date": "20260829", "pe_ttm": 30, "pb": 8},), None, "tushare", None, None,
        ))
        repository.save(StockDetail(
            "000001.SZ", "平安银行", "SZ", False, None, None, None, None, None, None,
            tuple(), None, None, None, None,
        ))

        tracked = repository.list_tracked()

    assert [item.ts_code for item in tracked] == ["600519.SH"]
    assert json.loads(json.dumps(tracked[0].valuation_history))[0]["pe_ttm"] == 30
