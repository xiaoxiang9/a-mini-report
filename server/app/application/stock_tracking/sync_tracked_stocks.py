from datetime import datetime, timezone

from app.application.stock_tracking.add_tracked_stock import AddTrackedStock
from app.domain.stock_tracking.providers import StockDataProvider
from app.domain.stock_tracking.repositories import StockTrackingRepository


class SyncTrackedStocks:
    def __init__(self, repository: StockTrackingRepository, provider: StockDataProvider) -> None:
        self._repository = repository
        self._provider = provider

    def execute(self) -> dict[str, object]:
        success: list[str] = []
        failures: list[dict[str, str]] = []
        for ts_code in self._repository.list_tracked_codes():
            try:
                AddTrackedStock(self._repository, self._provider).execute(ts_code)
                success.append(ts_code)
            except Exception as error:
                message = str(error)[:512] or error.__class__.__name__
                self._repository.save_sync_error(ts_code, message)
                failures.append({"ts_code": ts_code, "error": message})
        return {
            "started_at": datetime.now(timezone.utc),
            "success_count": len(success),
            "failure_count": len(failures),
            "success": success,
            "failures": failures,
        }
