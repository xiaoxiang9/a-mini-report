from typing import Protocol

from app.domain.platform.models import HomeSummary


class HomeSummaryRepository(Protocol):
    def find(self) -> HomeSummary: ...
