from dataclasses import dataclass
from datetime import datetime


def _name(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("TAG_NAME_REQUIRED")
    if len(value) > 64:
        raise ValueError("TAG_NAME_TOO_LONG")
    return value


@dataclass(frozen=True)
class TagCategory:
    id: int | None
    name: str
    sort_order: int = 0
    usage_count: int = 0
    created_at: datetime | None = None

    @classmethod
    def create(cls, name: str, sort_order: int = 0) -> "TagCategory":
        return cls(None, _name(name), sort_order)


@dataclass(frozen=True)
class TagDefinition:
    id: int | None
    category_id: int
    name: str
    sort_order: int = 0
    usage_count: int = 0
    category_name: str | None = None
    created_at: datetime | None = None

    @classmethod
    def create(cls, category_id: int, name: str, sort_order: int = 0) -> "TagDefinition":
        if category_id <= 0:
            raise ValueError("TAG_CATEGORY_REQUIRED")
        return cls(None, category_id, _name(name), sort_order)


@dataclass(frozen=True)
class StockTag:
    id: int
    category_id: int
    category_name: str
    name: str
