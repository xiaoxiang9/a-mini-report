from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class StockDetail:
    ts_code: str
    stock_name: str
    exchange: str
    is_tracked: bool
    current_price: float | None
    change_7d_percent: float | None
    pe_ttm: float | None
    pe_percentile: float | None
    pb: float | None
    pb_percentile: float | None
    valuation_history: tuple[dict[str, object], ...]
    latest_trade_date: date | None
    data_source: str | None
    last_synced_at: datetime | None
    sync_error: str | None
    history_start_date: date | None = None
    history_end_date: date | None = None
    history_count: int = 0
    tags: tuple[dict[str, object], ...] = ()
