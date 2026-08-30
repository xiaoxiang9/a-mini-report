from datetime import date

from app.application.stock_tracking.sync_tracked_stocks import SyncTrackedStocks
from app.domain.stock_tracking.models import StockDetail
from app.domain.stock_tracking.providers import StockSnapshot


class MemoryRepository:
    def __init__(self) -> None:
        self.items = {
            "600519.SH": StockDetail(
                "600519.SH", "贵州茅台", "SH", True, None, None, None, None, None, None,
                tuple(), None, None, None, None,
            ),
            "000001.SZ": StockDetail(
                "000001.SZ", "平安银行", "SZ", True, None, None, None, None, None, None,
                tuple(), None, None, None, None,
            ),
        }
        self.errors: dict[str, str] = {}

    def list_tracked_codes(self) -> list[str]:
        return list(self.items)

    def find_by_code(self, code: str) -> StockDetail | None:
        return self.items.get(code)

    def save(self, detail: StockDetail) -> StockDetail:
        self.items[detail.ts_code] = detail
        return detail

    def save_sync_error(self, code: str, error: str) -> None:
        self.errors[code] = error


class FakeProvider:
    def fetch_snapshot(self, ts_code: str, history: tuple[dict[str, object], ...]) -> StockSnapshot:
        if ts_code == "000001.SZ":
            raise RuntimeError("TUSHARE_RATE_LIMIT")
        return StockSnapshot(
            ts_code, "贵州茅台", "SH", date(2026, 8, 28), (100, 105, 110), 10, 2,
            ({"trade_date": "20260828", "pe_ttm": 10, "pb": 2},),
        )


def test_sync_continues_after_one_stock_fails() -> None:
    repository = MemoryRepository()
    result = SyncTrackedStocks(repository, FakeProvider()).execute()

    assert result["success"] == ["600519.SH"]
    assert result["failure_count"] == 1
    assert repository.errors == {"000001.SZ": "TUSHARE_RATE_LIMIT"}
    assert repository.items["600519.SH"].change_7d_percent == 10.0
