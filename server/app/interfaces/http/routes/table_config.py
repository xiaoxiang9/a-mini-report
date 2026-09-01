from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.domain.stock_tracking.table_config import TableColumn
from app.infrastructure.stock_tracking.table_config_repository import SqlAlchemyStockTableConfigRepository


class TableColumnPayload(BaseModel):
    key: str
    visible: bool = True
    frozen: bool = False
    searchable: bool = False
    searchType: str = "text"
    order: int = 0


def _payload(item: TableColumn) -> dict[str, object]:
    return {"key": item.key, "visible": item.visible, "frozen": item.frozen, "searchable": item.searchable,
            "searchType": item.search_type, "order": item.order}


def build_table_config_router(repository: SqlAlchemyStockTableConfigRepository) -> APIRouter:
    router = APIRouter()

    @router.get("/stocks/table-config")
    def get_config() -> list[dict[str, object]]:
        return [_payload(item) for item in repository.get()]

    @router.put("/stocks/table-config")
    def save_config(columns: list[TableColumnPayload]) -> list[dict[str, object]]:
        try:
            return [_payload(item) for item in repository.save([TableColumn(
                key=item.key, visible=item.visible, frozen=item.frozen, searchable=item.searchable,
                search_type=item.searchType, order=item.order,
            ) for item in columns])]
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    return router
