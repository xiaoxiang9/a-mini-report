import pytest

from app.domain.stock_tracking.table_config import TableColumn, validate_columns


def test_frozen_columns_must_be_a_contiguous_prefix():
    with pytest.raises(ValueError, match="FROZEN_COLUMNS_NOT_CONTIGUOUS"):
        validate_columns([TableColumn("name", True, False), TableColumn("tsCode", True, True)])


def test_operation_column_is_always_last_and_not_configurable():
    columns = validate_columns([TableColumn("stockName", True, False), TableColumn("operation", False, True)])
    assert columns[-1].key == "operation"
    assert columns[-1].visible is True
    assert columns[-1].frozen is True


def test_hidden_frozen_columns_do_not_break_visible_frozen_prefix():
    columns = validate_columns([
        TableColumn("stockName", True, True, order=0),
        TableColumn("tsCode", False, True, order=1),
        TableColumn("currentPrice", True, True, order=2),
    ])
    assert [item.key for item in columns[:3]] == ["stockName", "tsCode", "currentPrice"]
