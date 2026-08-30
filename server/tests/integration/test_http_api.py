from fastapi.testclient import TestClient

from app.domain.platform.models import FeatureEntry, HomeSummary
from app.interfaces.http.app import create_app


class StubHomeUseCase:
    def execute(self) -> HomeSummary:
        return HomeSummary(
            product_name="A股投资策略平台",
            tagline="用数据和纪律，建立可复盘的投资策略",
            status_text="平台已完成基础框架初始化",
            features=(
                FeatureEntry("daily-review", "每日复盘", "市场观察。", "available"),
            ),
        )


def test_health_and_home_summary_keep_existing_api_contract() -> None:
    client = TestClient(create_app(StubHomeUseCase(), lambda: "up"))

    assert client.get("/api/health").json() == {"status": "ok", "database": "up"}
    assert client.get("/api/home/summary").json() == {
        "productName": "A股投资策略平台",
        "tagline": "用数据和纪律，建立可复盘的投资策略",
        "statusText": "平台已完成基础框架初始化",
        "features": [
            {
                "key": "daily-review",
                "title": "每日复盘",
                "description": "市场观察。",
                "status": "available",
            }
        ],
    }
