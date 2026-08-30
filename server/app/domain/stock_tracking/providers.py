from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class StockSnapshot:
    ts_code: str
    stock_name: str
    exchange: str
    latest_trade_date: date
    prices: tuple[float, ...]
    pe_ttm: float | None
    pb: float | None
    valuation_history: tuple[dict[str, object], ...]


class StockDataProvider(Protocol):
    def fetch_snapshot(self, ts_code: str, history: tuple[dict[str, object], ...]) -> StockSnapshot: ...
