import re


def normalize_ts_code(value: str) -> str:
    raw = value.strip().upper()
    if "." in raw:
        code, exchange = raw.split(".", 1)
        if exchange not in {"SH", "SZ", "BJ"} or not re.fullmatch(r"\d{6}", code):
            raise ValueError("INVALID_TS_CODE")
        return f"{code}.{exchange}"
    if not re.fullmatch(r"\d{6}", raw):
        raise ValueError("INVALID_TS_CODE")
    if raw.startswith(("6", "68")):
        return f"{raw}.SH"
    if raw.startswith(("0", "3")):
        return f"{raw}.SZ"
    if raw.startswith(("4", "8")):
        return f"{raw}.BJ"
    raise ValueError("INVALID_TS_CODE")


def calculate_change_7d_percent(prices: list[float] | tuple[float, ...]) -> float | None:
    if len(prices) < 2 or prices[0] <= 0:
        return None
    return round((prices[-1] / prices[0] - 1) * 100, 4)


def calculate_percentile(value: float | None, history: list[float | None] | tuple[float | None, ...]) -> float | None:
    if value is None or value <= 0:
        return None
    valid = [item for item in history if item is not None and item > 0]
    if not valid:
        return None
    return round(sum(item <= value for item in valid) / len(valid) * 100, 4)
