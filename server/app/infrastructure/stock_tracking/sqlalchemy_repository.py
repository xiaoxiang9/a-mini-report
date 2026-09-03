import json
from datetime import date, datetime

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.domain.stock_tracking.models import StockDetail
from app.infrastructure.common.converters import safe_int


class SqlAlchemyStockTrackingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def _stock_tags(self, ts_code: str) -> tuple[dict[str, object], ...]:
        try:
            rows = self._session.execute(text("""
                SELECT t.id, t.categoryId, c.name AS categoryName, t.name
                FROM StockTagAssignment a JOIN StockTag t ON t.id=a.tagId
                JOIN StockTagCategory c ON c.id=t.categoryId WHERE a.tsCode=:ts_code
                ORDER BY c.sortOrder, t.sortOrder, t.id
            """), {"ts_code": ts_code}).mappings()
        except SQLAlchemyError:
            self._session.rollback()
            return ()
        return tuple({"id": int(r["id"]), "categoryId": int(r["categoryId"]),
                      "categoryName": r["categoryName"], "name": r["name"]} for r in rows)

    def _to_detail(self, row: dict) -> StockDetail:
        history = json.loads(row["valuationHistoryJson"] or "[]")
        return StockDetail(
            ts_code=row["tsCode"], stock_name=row["stockName"], exchange=row["exchange"],
            is_tracked=bool(row["isTracked"]), current_price=row["currentPrice"],
            change_7d_percent=row["change7dPercent"], pe_ttm=row["peTtm"],
            pe_percentile=row["pePercentile"], pb=row["pb"], pb_percentile=row["pbPercentile"],
            valuation_history=tuple(history), latest_trade_date=row["latestTradeDate"],
            data_source=row["dataSource"], last_synced_at=row["lastSyncedAt"],
            sync_error=row["syncError"],
            history_start_date=row.get("historyStartDate"),
            history_end_date=row.get("historyEndDate"),
            history_count=safe_int(row.get("historyCount")) or 0,
            tags=self._stock_tags(row["tsCode"]),
        )

    def _find(self, ts_code: str) -> StockDetail | None:
        row = self._session.execute(
            text("SELECT * FROM StockDetail WHERE tsCode = :ts_code"), {"ts_code": ts_code}
        ).mappings().first()
        return self._to_detail(dict(row)) if row else None

    def list_tracked(self) -> list[StockDetail]:
        rows = self._session.execute(
            text("SELECT * FROM StockDetail WHERE isTracked = TRUE ORDER BY stockName ASC, tsCode ASC")
        ).mappings()
        return [self._to_detail(dict(row)) for row in rows]

    def find_by_code(self, ts_code: str) -> StockDetail | None:
        return self._find(ts_code)

    def list_tracked_codes(self) -> list[str]:
        # Search can be called after a failed provider/database operation on the
        # long-lived application session. Clear that transaction before reading.
        self._session.rollback()
        rows = self._session.execute(
            text("SELECT tsCode FROM StockDetail WHERE isTracked = TRUE ORDER BY tsCode ASC")
        )
        return [row[0] for row in rows]

    def save(self, detail: StockDetail) -> StockDetail:
        values = {
            "ts_code": detail.ts_code, "stock_name": detail.stock_name, "exchange": detail.exchange,
            "is_tracked": detail.is_tracked, "current_price": detail.current_price,
            "change_7d_percent": detail.change_7d_percent, "pe_ttm": detail.pe_ttm,
            "pe_percentile": detail.pe_percentile, "pb": detail.pb, "pb_percentile": detail.pb_percentile,
            "history": json.dumps(detail.valuation_history, ensure_ascii=False),
            "latest_trade_date": detail.latest_trade_date, "data_source": detail.data_source,
            "last_synced_at": detail.last_synced_at, "sync_error": detail.sync_error,
            "history_start_date": detail.history_start_date, "history_end_date": detail.history_end_date,
            "history_count": detail.history_count,
        }
        if self._find(detail.ts_code):
            self._session.execute(text("""
                UPDATE StockDetail SET stockName=:stock_name, exchange=:exchange, isTracked=:is_tracked,
                currentPrice=:current_price, change7dPercent=:change_7d_percent, peTtm=:pe_ttm,
                pePercentile=:pe_percentile, pb=:pb, pbPercentile=:pb_percentile,
                valuationHistoryJson=:history, latestTradeDate=:latest_trade_date, dataSource=:data_source,
                lastSyncedAt=:last_synced_at, syncError=:sync_error, historyStartDate=:history_start_date,
                historyEndDate=:history_end_date, historyCount=:history_count WHERE tsCode=:ts_code
            """), values)
        else:
            self._session.execute(text("""
                INSERT INTO StockDetail
                (tsCode, stockName, exchange, isTracked, currentPrice, change7dPercent, peTtm,
                 pePercentile, pb, pbPercentile, valuationHistoryJson, latestTradeDate, dataSource,
                 lastSyncedAt, syncError, historyStartDate, historyEndDate, historyCount)
                VALUES (:ts_code, :stock_name, :exchange, :is_tracked, :current_price, :change_7d_percent,
                        :pe_ttm, :pe_percentile, :pb, :pb_percentile, :history, :latest_trade_date,
                        :data_source, :last_synced_at, :sync_error, :history_start_date, :history_end_date,
                        :history_count)
            """), values)
        self._session.commit()
        return self._find(detail.ts_code)  # type: ignore[return-value]

    def set_tracked(self, ts_code: str, is_tracked: bool) -> StockDetail | None:
        if not self._find(ts_code):
            return None
        self._session.execute(
            text("UPDATE StockDetail SET isTracked=:is_tracked WHERE tsCode=:ts_code"),
            {"ts_code": ts_code, "is_tracked": is_tracked},
        )
        self._session.commit()
        return self._find(ts_code)

    def save_sync_error(self, ts_code: str, error: str) -> None:
        self._session.execute(
            text("UPDATE StockDetail SET syncError=:error WHERE tsCode=:ts_code"),
            {"ts_code": ts_code, "error": error[:512]},
        )
        self._session.commit()
