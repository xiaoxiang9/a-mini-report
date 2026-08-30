from datetime import date

from fastapi.testclient import TestClient

from app.domain.stock_tracking.models import StockDetail
from app.domain.stock_tracking.providers import StockSnapshot
from app.interfaces.http.app import create_app


class MemoryStocks:
    def __init__(self) -> None:
        self.item = StockDetail(
            "600519.SH", "贵州茅台", "SH", True, 1500, 2.5, 30, 60, 8, 55,
            ({"trade_date": "20260829", "pe_ttm": 30, "pb": 8},), date(2026, 8, 29),
            "tushare", None, None,
        )

    def list_tracked(self):
        return [self.item] if self.item.is_tracked else []

    def list_tracked_codes(self):
        return [self.item.ts_code] if self.item.is_tracked else []

    def find_by_code(self, code):
        return self.item if code == self.item.ts_code else None

    def set_tracked(self, code, is_tracked):
        if not self.find_by_code(code):
            return None
        self.item = StockDetail(**{**self.item.__dict__, "is_tracked": is_tracked})
        return self.item

    def save(self, detail):
        self.item = detail
        return detail

    def save_sync_error(self, code, error):
        self.item = StockDetail(**{**self.item.__dict__, "sync_error": error})


class NoopProvider:
    def fetch_snapshot(self, ts_code, history):
        return StockSnapshot(ts_code, "贵州茅台", "SH", date(2026, 8, 29), (1500, 1510), 30, 8, history)


def test_stock_tracking_list_detail_and_remove() -> None:
    repository = MemoryStocks()
    client = TestClient(create_app(
        database_checker=lambda: "up",
        stock_repository=repository,
        stock_provider=NoopProvider(),
    ))

    assert client.get("/api/stocks/tracking").status_code == 200
    assert client.get("/api/stocks/600519").json()["tsCode"] == "600519.SH"
    response = client.delete("/api/stocks/600519.SH")
    assert response.status_code == 200
    assert response.json()["isTracked"] is False
