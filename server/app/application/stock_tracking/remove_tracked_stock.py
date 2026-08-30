from app.application.stock_tracking.calculations import normalize_ts_code
from app.domain.stock_tracking.models import StockDetail
from app.domain.stock_tracking.repositories import StockTrackingRepository


class RemoveTrackedStock:
    def __init__(self, repository: StockTrackingRepository) -> None:
        self._repository = repository

    def execute(self, ts_code: str) -> StockDetail | None:
        return self._repository.set_tracked(normalize_ts_code(ts_code), False)
