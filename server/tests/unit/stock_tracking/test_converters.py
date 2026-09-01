from app.infrastructure.common.converters import safe_float, safe_int


def test_numeric_converters_return_none_for_missing_or_invalid_values() -> None:
    assert safe_float(None) is None
    assert safe_float("not-a-number") is None
    assert safe_int(None) is None
    assert safe_int("not-an-integer") is None


def test_numeric_converters_keep_valid_values() -> None:
    assert safe_float("8.5") == 8.5
    assert safe_int("7") == 7
