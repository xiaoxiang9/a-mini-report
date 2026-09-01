import json

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.domain.stock_tracking.table_config import DEFAULT_COLUMNS, TableColumn, validate_columns


class SqlAlchemyStockTableConfigRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self) -> tuple[TableColumn, ...]:
        row = self.session.execute(text("SELECT configJson FROM StockTableConfig WHERE configKey='global'")) .mappings().first()
        if not row:
            return DEFAULT_COLUMNS
        try:
            return validate_columns([TableColumn(**item) for item in json.loads(row["configJson"])])
        except (TypeError, ValueError, json.JSONDecodeError):
            return DEFAULT_COLUMNS

    def save(self, columns: list[TableColumn]) -> tuple[TableColumn, ...]:
        normalized = validate_columns(columns)
        payload = json.dumps([item.__dict__ for item in normalized], ensure_ascii=False)
        self.session.execute(text("""
            INSERT INTO StockTableConfig (configKey, configJson) VALUES ('global', :config_json)
            ON DUPLICATE KEY UPDATE configJson=:config_json
        """), {"config_json": payload})
        self.session.commit()
        return normalized
