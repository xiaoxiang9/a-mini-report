from sqlalchemy import text
from sqlalchemy.orm import Session

from app.domain.tags.models import StockTag, TagCategory, TagDefinition


class SqlAlchemyTagRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_categories(self):
        rows = self.session.execute(text("""
            SELECT c.id, c.name, c.sortOrder,
                   COUNT(DISTINCT a.tsCode) AS usageCount
            FROM StockTagCategory c
            LEFT JOIN StockTag t ON t.categoryId = c.id
            LEFT JOIN StockTagAssignment a ON a.tagId = t.id
            GROUP BY c.id, c.name, c.sortOrder ORDER BY c.sortOrder, c.id
        """)).mappings()
        return [TagCategory(int(r["id"]), r["name"], int(r["sortOrder"]), int(r["usageCount"])) for r in rows]

    def list_tags(self):
        rows = self.session.execute(text("""
            SELECT t.id, t.categoryId, t.name, t.sortOrder, c.name AS categoryName,
                   COUNT(DISTINCT a.tsCode) AS usageCount
            FROM StockTag t JOIN StockTagCategory c ON c.id=t.categoryId
            LEFT JOIN StockTagAssignment a ON a.tagId=t.id
            GROUP BY t.id, t.categoryId, t.name, t.sortOrder, c.name ORDER BY t.sortOrder, t.id
        """)).mappings()
        return [TagDefinition(int(r["id"]), int(r["categoryId"]), r["name"], int(r["sortOrder"]), int(r["usageCount"]), r["categoryName"]) for r in rows]

    def create_category(self, category):
        result = self.session.execute(text("INSERT INTO StockTagCategory (name, sortOrder) VALUES (:name,:sort_order)"), {"name": category.name, "sort_order": category.sort_order})
        self.session.commit()
        return TagCategory(int(result.lastrowid), category.name, category.sort_order)

    def update_category(self, category_id, category):
        self.session.execute(text("UPDATE StockTagCategory SET name=:name, sortOrder=:sort_order WHERE id=:id"), {"id": category_id, "name": category.name, "sort_order": category.sort_order})
        self.session.commit()
        return TagCategory(category_id, category.name, category.sort_order)

    def delete_category(self, category_id):
        count = self.session.execute(text("SELECT COUNT(*) FROM StockTag WHERE categoryId=:id"), {"id": category_id}).scalar_one()
        if count:
            raise ValueError("TAG_CATEGORY_NOT_EMPTY")
        self.session.execute(text("DELETE FROM StockTagCategory WHERE id=:id"), {"id": category_id})
        self.session.commit()

    def create_tag(self, tag):
        result = self.session.execute(text("INSERT INTO StockTag (categoryId, name, sortOrder) VALUES (:category_id,:name,:sort_order)"), {"category_id": tag.category_id, "name": tag.name, "sort_order": tag.sort_order})
        self.session.commit()
        return TagDefinition(int(result.lastrowid), tag.category_id, tag.name, tag.sort_order)

    def update_tag(self, tag_id, tag):
        self.session.execute(text("UPDATE StockTag SET categoryId=:category_id, name=:name, sortOrder=:sort_order WHERE id=:id"), {"id": tag_id, "category_id": tag.category_id, "name": tag.name, "sort_order": tag.sort_order})
        self.session.commit()
        return TagDefinition(tag_id, tag.category_id, tag.name, tag.sort_order)

    def delete_tag(self, tag_id):
        if self.session.execute(text("SELECT COUNT(*) FROM StockTagAssignment WHERE tagId=:id"), {"id": tag_id}).scalar_one():
            raise ValueError("TAG_IN_USE")
        self.session.execute(text("DELETE FROM StockTag WHERE id=:id"), {"id": tag_id})
        self.session.commit()

    def list_stock_tags(self, ts_code):
        rows = self.session.execute(text("""
            SELECT t.id, t.categoryId, c.name AS categoryName, t.name
            FROM StockTagAssignment a JOIN StockTag t ON t.id=a.tagId
            JOIN StockTagCategory c ON c.id=t.categoryId WHERE a.tsCode=:ts_code
            ORDER BY c.sortOrder, t.sortOrder, t.id
        """), {"ts_code": ts_code}).mappings()
        return [StockTag(int(r["id"]), int(r["categoryId"]), r["categoryName"], r["name"]) for r in rows]

    def replace_stock_tags(self, ts_code, tag_ids):
        self.session.execute(text("DELETE FROM StockTagAssignment WHERE tsCode=:ts_code"), {"ts_code": ts_code})
        if tag_ids:
            for tag_id in tag_ids:
                self.session.execute(text("INSERT INTO StockTagAssignment (tsCode, tagId) SELECT :ts_code, id FROM StockTag WHERE id=:tag_id"), {"ts_code": ts_code, "tag_id": tag_id})
        self.session.commit()
        return self.list_stock_tags(ts_code)
