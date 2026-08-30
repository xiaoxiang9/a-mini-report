from app.domain.stock_tracking.models import StockDetail
from app.domain.stock_tracking.repositories import StockTrackingRepository


class ListTrackedStocks:
    def __init__(self, repository: StockTrackingRepository) -> None:
        self._repository = repository

    def execute(self) -> list[StockDetail]:
        return self._repository.list_tracked()
