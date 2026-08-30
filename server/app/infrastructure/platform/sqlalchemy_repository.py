from sqlalchemy import text
from sqlalchemy.orm import Session

from app.domain.platform.models import FeatureEntry, HomeSummary


class SqlAlchemyHomeSummaryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def find(self) -> HomeSummary:
        config = self._session.execute(
            text(
                "SELECT id, productName, tagline, statusText "
                "FROM PlatformConfig ORDER BY id ASC LIMIT 1"
            )
        ).mappings().first()
        if config is None:
            raise LookupError("HOME_SUMMARY_NOT_FOUND")

        features = self._session.execute(
            text(
                "SELECT `key`, title, description, status "
                "FROM FeatureEntry WHERE platformConfigId = :config_id "
                "ORDER BY sortOrder ASC, id ASC"
            ),
            {"config_id": config["id"]},
        ).mappings()
        return HomeSummary(
            product_name=config["productName"],
            tagline=config["tagline"],
            status_text=config["statusText"],
            features=tuple(
                FeatureEntry(
                    key=row["key"],
                    title=row["title"],
                    description=row["description"],
                    status=row["status"],
                )
                for row in features
            ),
        )
