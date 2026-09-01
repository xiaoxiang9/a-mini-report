from fastapi.testclient import TestClient

from app.interfaces.http.app import create_app


def test_table_config_put_is_allowed_by_cors_preflight():
    client = TestClient(create_app(
        home_use_case=object(),
        database_checker=lambda: "ok",
    ))
    response = client.options(
        "/api/stocks/table-config",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "PUT",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-methods"]
    assert "PUT" in response.headers["access-control-allow-methods"]
