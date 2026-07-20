import pytest
from commerce_platform.utils.shared import (
    merge_context,
    normalize_identifier,
    stable_sort_key,
)


def test_normalize_identifier_success():
    assert normalize_identifier("order 1001") == "ORDER_1001"


def test_normalize_identifier_invalid():
    with pytest.raises(ValueError):
        normalize_identifier("!!")


@pytest.mark.fragile
def test_normalize_identifier_uppercases():
    assert normalize_identifier("abc-9") == "ABC-9"


def test_merge_context_overrides():
    base = {"a": 1, "b": 2}
    extra = {"b": 3, "c": None}
    assert merge_context(base, extra) == {"a": 1, "b": 3}


def test_stable_sort_key_ordering():
    rows = [{"priority": 2, "id": "b"}, {"priority": 1, "id": "a"}]
    assert stable_sort_key(rows[0]) > stable_sort_key(rows[1])
