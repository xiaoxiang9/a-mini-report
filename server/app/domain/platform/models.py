from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureEntry:
    key: str
    title: str
    description: str
    status: str


@dataclass(frozen=True)
class HomeSummary:
    product_name: str
    tagline: str
    status_text: str
    features: tuple[FeatureEntry, ...]
