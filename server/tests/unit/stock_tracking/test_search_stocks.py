import pandas as pd

from app.application.stock_tracking.search_stocks import SearchStocks
from app.domain.stock_tracking.providers import StockSearchResult


class FakeProvider:
    def search_stocks(self, query: str):
        assert query == "贵州"
        return (StockSearchResult("600519.SH", "贵州茅台", "SSE"),)


class FakeRepository:
    def list_tracked_codes(self):
        return ["600519.SH"]


def test_search_returns_matching_stock_and_tracking_state() -> None:
    results = SearchStocks(FakeProvider(), FakeRepository()).execute("贵州")
    assert results == [{"tsCode": "600519.SH", "stockName": "贵州茅台", "exchange": "SSE", "isTracked": True}]
