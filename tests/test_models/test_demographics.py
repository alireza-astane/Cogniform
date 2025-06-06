import pytest
from pydantic import ValidationError
from cogniform.models.demographics import Demographics


def test_valid_demographics():
    demographics = Demographics(
        age=25,
        education="Bachelor's Degree",
        familiarity_with_cognitive_science="Intermediate",
    )
    assert demographics.age == 25
    assert demographics.education == "Bachelor's Degree"
    assert demographics.familiarity_with_cognitive_science == "Intermediate"


def test_missing_age():
    with pytest.raises(ValidationError) as exc_info:
        Demographics(
            education="Master's Degree", familiarity_with_cognitive_science="Advanced"
        )
    assert "Field required" in str(exc_info.value) or "field required" in str(
        exc_info.value
    )


def test_invalid_age_type():
    with pytest.raises(ValidationError) as exc_info:
        Demographics(
            age="twenty-five",
            education="High School",
            familiarity_with_cognitive_science="Basic",
        )
    assert "Input should be a valid integer" in str(
        exc_info.value
    ) or "validation error" in str(exc_info.value)


def test_missing_education():
    with pytest.raises(ValidationError) as exc_info:
        Demographics(age=30, familiarity_with_cognitive_science="None")
    assert "Field required" in str(exc_info.value) or "field required" in str(
        exc_info.value
    )


def test_missing_familiarity():
    with pytest.raises(ValidationError) as exc_info:
        Demographics(age=28, education="PhD")
    assert "Field required" in str(exc_info.value) or "field required" in str(
        exc_info.value
    )
