from dataclasses import dataclass


@dataclass(frozen=True)
class TableColumn:
    key: str
    visible: bool = True
    frozen: bool = False
    searchable: bool = False
    search_type: str = "text"
    order: int = 0


DEFAULT_COLUMNS = (
    TableColumn("stockName", True, True, True, "text", 0),
    TableColumn("tsCode", True, True, True, "text", 1),
    TableColumn("currentPrice", True, False, True, "number", 2),
    TableColumn("change7dPercent", True, False, True, "number", 3),
    TableColumn("peTtm", True, False, True, "number", 4),
    TableColumn("pePercentile", True, False, True, "number", 5),
    TableColumn("pb", True, False, True, "number", 6),
    TableColumn("pbPercentile", True, False, True, "number", 7),
    TableColumn("latestTradeDate", True, False, False, "text", 8),
    TableColumn("dataSource", True, False, False, "enum", 9),
    TableColumn("operation", True, True, False, "none", 10),
)


def validate_columns(columns: list[TableColumn]) -> tuple[TableColumn, ...]:
    if not columns:
        raise ValueError("TABLE_COLUMNS_EMPTY")
    submitted = sorted(columns, key=lambda item: item.order)
    fixed = {
        "stockName": TableColumn("stockName", True, True, True, "text", 0),
        "tsCode": TableColumn("tsCode", True, True, True, "text", 1),
    }
    for key, expected in fixed.items():
        item = next((candidate for candidate in submitted if candidate.key == key), None)
        if item is not None and item != expected:
            raise ValueError("IDENTITY_COLUMNS_LOCKED")
    normalized = list(fixed.values())
    normalized.extend(
        TableColumn(item.key, item.visible, item.frozen, item.searchable, item.search_type, order)
        for order, item in enumerate((item for item in submitted if item.key not in fixed and item.key != "operation"), start=2)
    )
    operation = next((item for item in normalized if item.key == "operation"), None)
    if operation is None:
        normalized.append(TableColumn("operation", True, True, False, "none", len(normalized)))
    else:
        normalized = [item for item in normalized if item.key != "operation"]
        normalized.append(TableColumn("operation", True, True, False, "none", len(normalized)))
    if not any(item.visible and item.key in {"stockName", "tsCode"} for item in normalized):
        raise ValueError("IDENTITY_COLUMN_REQUIRED")
    frozen_seen_gap = False
    for item in normalized[:-1]:
        if not item.visible:
            continue
        if not item.frozen:
            frozen_seen_gap = True
        elif frozen_seen_gap:
            raise ValueError("FROZEN_COLUMNS_NOT_CONTIGUOUS")
    return tuple(normalized)
