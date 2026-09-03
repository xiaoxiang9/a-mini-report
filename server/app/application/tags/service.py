from __future__ import annotations

from app.domain.tags.models import TagCategory, TagDefinition
from app.domain.tags.repositories import TagRepository


class TagManagementService:
    def __init__(self, repository: TagRepository) -> None:
        self.repository = repository

    def list(self) -> list[dict[str, object]]:
        categories = self.repository.list_categories()
        tags = self.repository.list_tags()
        return [{
            "id": category.id, "name": category.name, "sortOrder": category.sort_order,
            "usageCount": category.usage_count,
            "tags": [{"id": tag.id, "categoryId": tag.category_id, "categoryName": category.name,
                      "name": tag.name, "sortOrder": tag.sort_order, "usageCount": tag.usage_count}
                     for tag in tags if tag.category_id == category.id],
        } for category in categories]

    def create_category(self, name: str, sort_order: int = 0) -> TagCategory:
        return self.repository.create_category(TagCategory.create(name, sort_order))

    def update_category(self, category_id: int, name: str, sort_order: int = 0) -> TagCategory:
        return self.repository.update_category(category_id, TagCategory(category_id, name.strip(), sort_order))

    def delete_category(self, category_id: int) -> None:
        return self.repository.delete_category(category_id)

    def create_tag(self, category_id: int, name: str, sort_order: int = 0) -> TagDefinition:
        return self.repository.create_tag(TagDefinition.create(category_id, name, sort_order))

    def update_tag(self, tag_id: int, category_id: int, name: str, sort_order: int = 0) -> TagDefinition:
        return self.repository.update_tag(tag_id, TagDefinition(tag_id, category_id, name.strip(), sort_order))

    def delete_tag(self, tag_id: int) -> None:
        return self.repository.delete_tag(tag_id)

    def list_stock_tags(self, ts_code: str):
        return self.repository.list_stock_tags(ts_code)

    def replace_stock_tags(self, ts_code: str, tag_ids: list[int]):
        return self.repository.replace_stock_tags(ts_code, sorted(set(tag_ids)))
