import pytest

from validators import (
    ValidationError,
    ALLOWED_ANALYSIS_TYPES,
    ensure_unique_names,
    validate_entity,
    validate_filename,
    validate_analysis_type,
)


def test_unique_names_ok():
    items = [{"name": "A"}, {"name": "B"}]
    assert ensure_unique_names(items) == items


def test_unique_names_duplicate():
    items = [{"name": "A"}, {"name": "A"}]
    with pytest.raises(ValidationError):
        ensure_unique_names(items)


def test_validate_entity_kind():
    assert validate_entity({"entity_kind": "node"}) == {"entity_kind": "node"}
    with pytest.raises(ValidationError):
        validate_entity({"entity_kind": "element"})
    assert validate_entity({"entity_kind": "element", "element_type": "shell"}) == {
        "entity_kind": "element",
        "element_type": "shell",
    }
    with pytest.raises(ValidationError):
        validate_entity({"entity_kind": "invalid"})


def test_validate_filename():
    assert validate_filename("123") == "123"
    with pytest.raises(ValidationError):
        validate_filename("12a")


def test_validate_analysis_type():
    for atype in ALLOWED_ANALYSIS_TYPES:
        assert validate_analysis_type(atype) == atype
    with pytest.raises(ValidationError):
        validate_analysis_type("unknown")
