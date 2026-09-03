from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.application.tags.service import TagManagementService


class NamePayload(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    sortOrder: int = 0


class TagPayload(NamePayload):
    categoryId: int = Field(gt=0)


class StockTagsPayload(BaseModel):
    tagIds: list[int] = []


def _tag(item):
    return {"id": item.id, "categoryId": item.category_id, "categoryName": item.category_name, "name": item.name}


def _category(item):
    return {"id": item.id, "name": item.name, "sortOrder": item.sort_order, "usageCount": item.usage_count}


def _definition(item):
    return {"id": item.id, "categoryId": item.category_id, "categoryName": item.category_name,
            "name": item.name, "sortOrder": item.sort_order, "usageCount": item.usage_count}


def build_tags_router(service: TagManagementService) -> APIRouter:
    router = APIRouter()

    @router.get("/tags")
    def list_tags(): return service.list()

    @router.post("/tags/categories", status_code=201)
    def create_category(payload: NamePayload):
        try: return _category(service.create_category(payload.name, payload.sortOrder))
        except ValueError as error: raise HTTPException(422, str(error)) from error

    @router.patch("/tags/categories/{category_id}")
    def update_category(category_id: int, payload: NamePayload):
        try: return _category(service.update_category(category_id, payload.name, payload.sortOrder))
        except ValueError as error: raise HTTPException(422, str(error)) from error

    @router.delete("/tags/categories/{category_id}")
    def delete_category(category_id: int):
        try: service.delete_category(category_id); return {"ok": True}
        except ValueError as error: raise HTTPException(409, str(error)) from error

    @router.post("/tags", status_code=201)
    def create_tag(payload: TagPayload):
        try: return _definition(service.create_tag(payload.categoryId, payload.name, payload.sortOrder))
        except ValueError as error: raise HTTPException(422, str(error)) from error

    @router.patch("/tags/{tag_id}")
    def update_tag(tag_id: int, payload: TagPayload):
        try: return _definition(service.update_tag(tag_id, payload.categoryId, payload.name, payload.sortOrder))
        except ValueError as error: raise HTTPException(422, str(error)) from error

    @router.delete("/tags/{tag_id}")
    def delete_tag(tag_id: int):
        try: service.delete_tag(tag_id); return {"ok": True}
        except ValueError as error: raise HTTPException(409, str(error)) from error

    @router.get("/stocks/{ts_code}/tags")
    def stock_tags(ts_code: str): return [_tag(item) for item in service.list_stock_tags(ts_code)]

    @router.put("/stocks/{ts_code}/tags")
    def replace_stock_tags(ts_code: str, payload: StockTagsPayload):
        return [_tag(item) for item in service.replace_stock_tags(ts_code, payload.tagIds)]

    return router
