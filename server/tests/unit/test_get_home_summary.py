from dataclasses import dataclass

from app.application.home.get_home_summary import GetHomeSummary
from app.domain.platform.models import FeatureEntry, HomeSummary


@dataclass
class InMemoryHomeSummaryRepository:
    summary: HomeSummary

    def find(self) -> HomeSummary:
        return self.summary


def test_get_home_summary_returns_repository_summary() -> None:
    expected = HomeSummary(
        product_name="A股投资策略平台",
        tagline="用数据和纪律，建立可复盘的投资策略",
        status_text="平台已完成基础框架初始化",
        features=(
            FeatureEntry(
                key="daily-review",
                title="每日复盘",
                description="沉淀市场观察、板块强弱与交易计划。",
                status="available",
            ),
        ),
    )

    result = GetHomeSummary(InMemoryHomeSummaryRepository(expected)).execute()

    assert result == expected
