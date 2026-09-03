import pytest

from app.domain.tags.models import TagCategory, TagDefinition


def test_tag_category_requires_non_empty_name() -> None:
    with pytest.raises(ValueError, match="TAG_NAME_REQUIRED"):
        TagCategory.create(" ")


def test_tag_definition_requires_category_and_non_empty_name() -> None:
    with pytest.raises(ValueError, match="TAG_NAME_REQUIRED"):
        TagDefinition.create(1, "")


def test_tag_definition_can_be_created_with_trimmed_name() -> None:
    tag = TagDefinition.create(3, "  核心资产  ")
    assert tag.category_id == 3
    assert tag.name == "核心资产"
