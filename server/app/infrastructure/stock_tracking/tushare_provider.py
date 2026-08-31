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
        basic = self._pro.stock_basic(ts_code=ts_code, fields="ts_code,name,exchange,list_date")
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
        calendar_latest_date = trade_dates[-1]
        list_date = str(stock["list_date"])
        if not list_date or list_date.lower() == "nan":
            raise LookupError("LIST_DATE_MISSING")
        history_frame = self._fetch_valuation_history(list_date, calendar_latest_date, ts_code)
        if history_frame.empty:
            latest_trade_date = calendar_latest_date
        else:
            latest_trade_date = str(history_frame["trade_date"].astype(str).max())

        daily = self._pro.daily(ts_code=ts_code, start_date=start, end_date=calendar_latest_date)
        daily = daily.sort_values("trade_date")
        daily = daily[daily["trade_date"].astype(str) <= latest_trade_date]
        prices = tuple(float(value) for value in daily.tail(7)["close"].tolist())
        row = history_frame[history_frame["trade_date"].astype(str) == latest_trade_date].iloc[0] if not history_frame.empty else None
        pe_ttm = float(row["pe_ttm"]) if row is not None and row.get("pe_ttm") == row.get("pe_ttm") else None
        pb = float(row["pb"]) if row is not None and row.get("pb") == row.get("pb") else None
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
            history_start_date=datetime.strptime(list_date, "%Y%m%d").date(),
            history_end_date=datetime.strptime(latest_trade_date, "%Y%m%d").date(),
            history_count=len(merged),
        )

    def _fetch_valuation_history(self, start_date: str, end_date: str, ts_code: str):
        import pandas as pd

        start = datetime.strptime(start_date, "%Y%m%d").date()
        end = datetime.strptime(end_date, "%Y%m%d").date()
        frames = []
        cursor = start
        while cursor <= end:
            segment_end = min(cursor + timedelta(days=364), end)
            frame = self._pro.daily_basic(
                ts_code=ts_code,
                start_date=cursor.strftime("%Y%m%d"),
                end_date=segment_end.strftime("%Y%m%d"),
            )
            if not frame.empty:
                frames.append(frame)
            cursor = segment_end + timedelta(days=1)
        if not frames:
            return pd.DataFrame(columns=["trade_date", "pe_ttm", "pb"])
        return pd.concat(frames, ignore_index=True).drop_duplicates(subset=["trade_date"]).sort_values("trade_date")
