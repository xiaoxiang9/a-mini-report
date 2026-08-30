from datetime import date, datetime, timedelta

from app.domain.stock_tracking.providers import StockDataProvider, StockSnapshot


class TushareStockDataProvider(StockDataProvider):
    def __init__(self, token: str | None) -> None:
        if not token:
            raise RuntimeError("TUSHARE_TOKEN_MISSING")
        try:
            import tushare
        except ImportError as error:
            raise RuntimeError("TUSHARE_PACKAGE_MISSING") from error

        self._pro = tushare.pro_api(token)

    def fetch_snapshot(self, ts_code: str, history: tuple[dict[str, object], ...]) -> StockSnapshot:
        basic = self._pro.stock_basic(ts_code=ts_code, fields="ts_code,name,exchange")
        if basic.empty:
            raise LookupError("STOCK_NOT_FOUND")
        stock = basic.iloc[0]
        today = date.today()
        start = (today - timedelta(days=30)).strftime("%Y%m%d")
        end = today.strftime("%Y%m%d")
        calendar = self._pro.trade_cal(exchange="", start_date=start, end_date=end, is_open="1")
        if calendar.empty:
            raise LookupError("NO_RECENT_TRADE_DATE")
        trade_dates = sorted(calendar["cal_date"].astype(str).tolist())
        latest_trade_date = trade_dates[-1]
        daily = self._pro.daily(ts_code=ts_code, start_date=start, end_date=latest_trade_date)
        daily = daily.sort_values("trade_date")
        prices = tuple(float(value) for value in daily.tail(7)["close"].tolist())
        basic_daily = self._pro.daily_basic(ts_code=ts_code, trade_date=latest_trade_date)
        row = basic_daily.iloc[0] if not basic_daily.empty else None
        pe_ttm = float(row["pe_ttm"]) if row is not None and row.get("pe_ttm") == row.get("pe_ttm") else None
        pb = float(row["pb"]) if row is not None and row.get("pb") == row.get("pb") else None
        history_frame = self._pro.daily_basic(ts_code=ts_code, start_date="20100101", end_date=latest_trade_date)
        history_rows = [
            {"trade_date": str(item.trade_date), "pe_ttm": None if item.pe_ttm != item.pe_ttm else float(item.pe_ttm), "pb": None if item.pb != item.pb else float(item.pb)}
            for item in history_frame.itertuples(index=False)
        ]
        merged = {str(item["trade_date"]): item for item in history}
        merged.update({str(item["trade_date"]): item for item in history_rows})
        return StockSnapshot(
            ts_code=ts_code, stock_name=str(stock["name"]), exchange=str(stock["exchange"]),
            latest_trade_date=datetime.strptime(latest_trade_date, "%Y%m%d").date(), prices=prices,
            pe_ttm=pe_ttm, pb=pb, valuation_history=tuple(merged[key] for key in sorted(merged)),
        )
