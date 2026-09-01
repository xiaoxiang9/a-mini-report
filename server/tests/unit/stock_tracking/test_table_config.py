import pytest

from app.domain.stock_tracking.table_config import TableColumn, validate_columns


def test_frozen_columns_must_be_a_contiguous_prefix():
    with pytest.raises(ValueError, match="FROZEN_COLUMNS_NOT_CONTIGUOUS"):
        validate_columns([
            TableColumn("stockName", True, True, True, "text", 0),
            TableColumn("tsCode", True, True, True, "text", 1),
            TableColumn("currentPrice", True, False, order=2),
            TableColumn("change7dPercent", True, True, order=3),
        ])


def test_operation_column_is_always_last_and_not_configurable():
    columns = validate_columns([
        TableColumn("stockName", True, True, True, "text", 0),
        TableColumn("tsCode", True, True, True, "text", 1),
        TableColumn("operation", False, True),
    ])
    assert columns[-1].key == "operation"
    assert columns[-1].visible is True
    assert columns[-1].frozen is True


def test_identity_columns_are_always_visible_frozen_and_searchable():
    columns = validate_columns([TableColumn("currentPrice")])
    assert [(item.key, item.visible, item.frozen, item.searchable) for item in columns[:2]] == [
        ("stockName", True, True, True),
        ("tsCode", True, True, True),
    ]


def test_identity_columns_cannot_be_modified():
    with pytest.raises(ValueError, match="IDENTITY_COLUMNS_LOCKED"):
        validate_columns([TableColumn("stockName", True, False), TableColumn("tsCode")])


def test_unknown_columns_are_rejected():
    with pytest.raises(ValueError, match="UNKNOWN_TABLE_COLUMN"):
        validate_columns([TableColumn("stockName", True, True, True, "text", 0), TableColumn("tsCode", True, True, True, "text", 1), TableColumn("legacyMetric", order=2)])


def test_hidden_frozen_columns_do_not_break_visible_frozen_prefix():
    columns = validate_columns([
        TableColumn("stockName", True, True, True, "text", 0),
        TableColumn("tsCode", True, True, True, "text", 1),
        TableColumn("currentPrice", False, True, order=2),
        TableColumn("change7dPercent", True, True, order=3),
    ])
    assert [item.key for item in columns[:4]] == ["stockName", "tsCode", "currentPrice", "change7dPercent"]
