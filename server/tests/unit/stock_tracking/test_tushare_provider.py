from datetime import date

import pandas as pd

from app.infrastructure.stock_tracking.tushare_provider import TushareStockDataProvider


class FakePro:
    def stock_basic(self, **kwargs):
        return pd.DataFrame([{"ts_code": "600519.SH", "name": "贵州茅台", "exchange": "SSE"}])

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


def test_provider_uses_latest_available_valuation_date() -> None:
    provider = object.__new__(TushareStockDataProvider)
    provider._pro = FakePro()

    snapshot = provider.fetch_snapshot("600519.SH", tuple())

    assert snapshot.latest_trade_date == date(2026, 8, 28)
    assert snapshot.pe_ttm == 19.9162
    assert snapshot.pb == 6.4551
    assert snapshot.prices == (1290.0,)
