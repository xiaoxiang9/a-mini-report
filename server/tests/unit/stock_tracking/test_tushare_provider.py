from datetime import date

import pandas as pd

from app.infrastructure.stock_tracking.tushare_provider import TushareStockDataProvider


class FakePro:
    def stock_basic(self, **kwargs):
        return pd.DataFrame([{"ts_code": "600519.SH", "name": "贵州茅台", "exchange": "SSE", "list_date": "20200101"}])

    def trade_cal(self, **kwargs):
        return pd.DataFrame([{"cal_date": "20260828"}, {"cal_date": "20260831"}])

    def daily(self, **kwargs):
        return pd.DataFrame([
            {"trade_date": "20260828", "close": 1290},
            {"trade_date": "20260831", "close": 1297.4},
        ])

    def daily_basic(self, **kwargs):
        if "trade_date" in kwargs:
            return pd.DataFrame(columns=["trade_date", "pe_ttm", "pb"])
        return pd.DataFrame([
            {"trade_date": "20260827", "pe_ttm": 20.0, "pb": 6.4},
            {"trade_date": "20260828", "pe_ttm": 19.9162, "pb": 6.4551},
        ])


class MissingValuationPro(FakePro):
    def daily_basic(self, **kwargs):
        return pd.DataFrame([{"trade_date": "20260828", "pe_ttm": None, "pb": None}])


def test_provider_uses_latest_available_valuation_date() -> None:
    provider = object.__new__(TushareStockDataProvider)
    provider._pro = FakePro()

    snapshot = provider.fetch_snapshot("600519.SH", tuple())

    assert snapshot.latest_trade_date == date(2026, 8, 28)
    assert snapshot.pe_ttm == 19.9162
    assert snapshot.pb == 6.4551
    assert snapshot.prices == (1290.0,)
    assert snapshot.history_start_date == date(2020, 1, 1)
    assert snapshot.history_count == 2


def test_provider_searches_stock_code_or_name() -> None:
    provider = TushareStockDataProvider.__new__(TushareStockDataProvider)
    provider._pro = FakePro()
    results = provider.search_stocks("贵州")
    assert results[0].ts_code == "600519.SH"


def test_provider_treats_missing_valuation_values_as_empty() -> None:
    provider = object.__new__(TushareStockDataProvider)
    provider._pro = MissingValuationPro()

    snapshot = provider.fetch_snapshot("600519.SH", tuple())

    assert snapshot.pe_ttm is None
    assert snapshot.pb is None
    assert snapshot.valuation_history[0]["pe_ttm"] is None
    assert snapshot.valuation_history[0]["pb"] is None
