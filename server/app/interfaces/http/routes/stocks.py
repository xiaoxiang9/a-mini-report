from typing import Annotated

from fastapi import APIRouter, HTTPException, Path
from pydantic import AliasChoices, BaseModel, Field

from app.application.stock_tracking.add_tracked_stock import AddTrackedStock
from app.application.stock_tracking.calculations import normalize_ts_code
from app.application.stock_tracking.get_stock_detail import GetStockDetail
from app.application.stock_tracking.list_tracked_stocks import ListTrackedStocks
from app.application.stock_tracking.remove_tracked_stock import RemoveTrackedStock
from app.application.stock_tracking.sync_tracked_stocks import SyncTrackedStocks
from app.domain.stock_tracking.models import StockDetail


class TrackStockRequest(BaseModel):
    ts_code: str = Field(validation_alias=AliasChoices("tsCode", "ts_code"))


class StockResponse(BaseModel):
    tsCode: str
    stockName: str
    exchange: str
    isTracked: bool
    currentPrice: float | None
    change7dPercent: float | None
    peTtm: float | None
    pePercentile: float | None
    pb: float | None
    pbPercentile: float | None
    valuationHistory: list[dict[str, object]]
    latestTradeDate: str | None
    dataSource: str | None
    lastSyncedAt: str | None
    syncError: str | None


def _response(detail: StockDetail) -> StockResponse:
    return StockResponse(
        tsCode=detail.ts_code, stockName=detail.stock_name, exchange=detail.exchange,
        isTracked=detail.is_tracked, currentPrice=detail.current_price,
        change7dPercent=detail.change_7d_percent, peTtm=detail.pe_ttm,
        pePercentile=detail.pe_percentile, pb=detail.pb, pbPercentile=detail.pb_percentile,
        valuationHistory=list(detail.valuation_history),
        latestTradeDate=detail.latest_trade_date.isoformat() if detail.latest_trade_date else None,
        dataSource=detail.data_source,
        lastSyncedAt=detail.last_synced_at.isoformat() if detail.last_synced_at else None,
        syncError=detail.sync_error,
    )


def build_stocks_router(
    list_use_case: ListTrackedStocks,
    get_use_case: GetStockDetail,
    add_use_case: AddTrackedStock,
    remove_use_case: RemoveTrackedStock,
    sync_use_case: SyncTrackedStocks,
) -> APIRouter:
    router = APIRouter()

    @router.get("/stocks/tracking", response_model=list[StockResponse])
    def list_stocks() -> list[StockResponse]:
        return [_response(item) for item in list_use_case.execute()]

    @router.get("/stocks/{ts_code}", response_model=StockResponse)
    def get_stock(ts_code: Annotated[str, Path(min_length=6, max_length=10)]) -> StockResponse:
        try:
            detail = get_use_case.execute(ts_code)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        if detail is None:
            raise HTTPException(status_code=404, detail="STOCK_NOT_FOUND")
        return _response(detail)

    @router.post("/stocks/tracking", response_model=StockResponse, status_code=201)
    def add_stock(payload: TrackStockRequest) -> StockResponse:
        try:
            return _response(add_use_case.execute(payload.ts_code))
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        except LookupError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error
        except RuntimeError as error:
            raise HTTPException(status_code=503, detail=str(error)) from error

    @router.delete("/stocks/{ts_code}", response_model=StockResponse)
    def remove_stock(ts_code: str) -> StockResponse:
        try:
            detail = remove_use_case.execute(ts_code)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        if detail is None:
            raise HTTPException(status_code=404, detail="STOCK_NOT_FOUND")
        return _response(detail)

    @router.post("/stocks/sync")
    def sync_stocks() -> dict[str, object]:
        return sync_use_case.execute()

    return router
