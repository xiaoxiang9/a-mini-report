from fastapi.testclient import TestClient

from app.domain.tags.models import StockTag, TagCategory, TagDefinition
from app.interfaces.http.app import create_app


class MemoryTags:
    def __init__(self) -> None:
        self.categories = [TagCategory(1, "风格")]
        self.tags = [TagDefinition(1, 1, "价值")]
        self.assignments = {"600519.SH": [1]}

    def list_categories(self): return [TagCategory(c.id, c.name, c.sort_order, sum(1 for ids in self.assignments.values() if ids)) for c in self.categories]
    def list_tags(self): return [TagDefinition(t.id, t.category_id, t.name, t.sort_order, sum(t.id in ids for ids in self.assignments.values()), t.category_name) for t in self.tags]
    def create_category(self, category): return TagCategory(2, category.name)
    def update_category(self, category_id, category): return TagCategory(category_id, category.name)
    def delete_category(self, category_id): return None
    def create_tag(self, tag): return TagDefinition(2, tag.category_id, tag.name)
    def update_tag(self, tag_id, tag): return TagDefinition(tag_id, tag.category_id, tag.name)
    def delete_tag(self, tag_id):
        if any(tag_id in ids for ids in self.assignments.values()):
            raise ValueError("TAG_IN_USE")
    def list_stock_tags(self, ts_code):
        return [StockTag(tag.id, tag.category_id, "风格", tag.name) for tag in self.tags if tag.id in self.assignments.get(ts_code, [])]
    def replace_stock_tags(self, ts_code, tag_ids):
        self.assignments[ts_code] = tag_ids
        return self.list_stock_tags(ts_code)


def test_tag_routes_list_nested_data_and_reject_used_tag_delete() -> None:
    tags = MemoryTags()
    client = TestClient(create_app(database_checker=lambda: "up", tag_repository=tags))
    response = client.get("/api/tags")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "风格", "sortOrder": 0, "usageCount": 1, "tags": [{"id": 1, "categoryId": 1, "categoryName": "风格", "name": "价值", "sortOrder": 0, "usageCount": 1}]}]
    assert client.delete("/api/tags/1").status_code == 409


def test_stock_tag_routes_replace_assignments() -> None:
    tags = MemoryTags()
    client = TestClient(create_app(database_checker=lambda: "up", tag_repository=tags))
    response = client.put("/api/stocks/600519.SH/tags", json={"tagIds": []})
    assert response.status_code == 200
    assert response.json() == []
