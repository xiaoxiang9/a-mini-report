from app.domain.stock_tracking.providers import StockDataProvider
from app.domain.stock_tracking.repositories import StockTrackingRepository


class SearchStocks:
    def __init__(self, provider: StockDataProvider, repository: StockTrackingRepository) -> None:
        self._provider = provider
        self._repository = repository

    def execute(self, query: str) -> list[dict[str, object]]:
        keyword = query.strip()
        if not keyword:
            return []
        tracked = set(self._repository.list_tracked_codes())
        return [
            {"tsCode": item.ts_code, "stockName": item.stock_name, "exchange": item.exchange,
             "isTracked": item.ts_code in tracked}
            for item in self._provider.search_stocks(keyword)
        ]
