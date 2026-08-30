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


def test_local_web_origin_can_call_api() -> None:
    client = TestClient(create_app(StubHomeUseCase(), lambda: "up"))

    response = client.options(
        "/api/stocks/tracking",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"
