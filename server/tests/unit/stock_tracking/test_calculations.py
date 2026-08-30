from app.application.stock_tracking.calculations import (
    calculate_change_7d_percent,
    calculate_percentile,
    normalize_ts_code,
)


def test_normalize_ts_code_adds_exchange_for_supported_code() -> None:
    assert normalize_ts_code("600519") == "600519.SH"
    assert normalize_ts_code("000001.sz") == "000001.SZ"


def test_calculate_change_7d_uses_first_and_latest_trading_close() -> None:
    assert calculate_change_7d_percent([100, 102, 101, 104, 105, 108, 110]) == 10.0
    assert calculate_change_7d_percent([100]) is None


def test_calculate_percentile_ignores_invalid_values() -> None:
    assert calculate_percentile(10, [None, 5, 10, 20, -1]) == 66.6667
    assert calculate_percentile(7, [5, 10, 20]) == 33.3333
    assert calculate_percentile(None, [5, 10]) is None
