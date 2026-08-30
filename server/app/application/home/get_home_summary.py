from app.domain.platform.models import HomeSummary
from app.domain.platform.repositories import HomeSummaryRepository


class GetHomeSummary:
    def __init__(self, repository: HomeSummaryRepository) -> None:
        self._repository = repository

    def execute(self) -> HomeSummary:
        return self._repository.find()
