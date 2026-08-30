from datetime import datetime, timezone

from app.application.stock_tracking.calculations import calculate_change_7d_percent, calculate_percentile, normalize_ts_code
from app.domain.stock_tracking.models import StockDetail
from app.domain.stock_tracking.providers import StockDataProvider
from app.domain.stock_tracking.repositories import StockTrackingRepository


class AddTrackedStock:
    def __init__(self, repository: StockTrackingRepository, provider: StockDataProvider) -> None:
        self._repository = repository
        self._provider = provider

    def execute(self, ts_code: str) -> StockDetail:
        code = normalize_ts_code(ts_code)
        previous = self._repository.find_by_code(code)
        history = previous.valuation_history if previous else tuple()
        snapshot = self._provider.fetch_snapshot(code, history)
        pe_values = tuple(item.get("pe_ttm") for item in snapshot.valuation_history)
        pb_values = tuple(item.get("pb") for item in snapshot.valuation_history)
        detail = StockDetail(
            ts_code=code, stock_name=snapshot.stock_name, exchange=snapshot.exchange, is_tracked=True,
            current_price=snapshot.prices[-1] if snapshot.prices else None,
            change_7d_percent=calculate_change_7d_percent(snapshot.prices),
            pe_ttm=snapshot.pe_ttm, pe_percentile=calculate_percentile(snapshot.pe_ttm, pe_values),
            pb=snapshot.pb, pb_percentile=calculate_percentile(snapshot.pb, pb_values),
            valuation_history=snapshot.valuation_history, latest_trade_date=snapshot.latest_trade_date,
            data_source="tushare", last_synced_at=datetime.now(timezone.utc), sync_error=None,
        )
        return self._repository.save(detail)
