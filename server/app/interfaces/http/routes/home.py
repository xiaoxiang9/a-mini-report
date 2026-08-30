from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.application.home.get_home_summary import GetHomeSummary


class FeatureResponse(BaseModel):
    key: str
    title: str
    description: str
    status: str


class HomeSummaryResponse(BaseModel):
    productName: str
    tagline: str
    statusText: str
    features: list[FeatureResponse]


def build_home_router(use_case: GetHomeSummary) -> APIRouter:
    router = APIRouter()

    @router.get("/home/summary", response_model=HomeSummaryResponse)
    def home_summary() -> HomeSummaryResponse:
        try:
            result = use_case.execute()
        except LookupError as error:
            raise HTTPException(status_code=404, detail="HOME_SUMMARY_NOT_FOUND") from error
        return HomeSummaryResponse(
            productName=result.product_name,
            tagline=result.tagline,
            statusText=result.status_text,
            features=[
                FeatureResponse(
                    key=feature.key,
                    title=feature.title,
                    description=feature.description,
                    status=feature.status,
                )
                for feature in result.features
            ],
        )

    return router
