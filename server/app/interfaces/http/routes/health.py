from collections.abc import Callable

from fastapi import APIRouter


def build_health_router(database_checker: Callable[[], str]) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "database": database_checker()}

    return router
