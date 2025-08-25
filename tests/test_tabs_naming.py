from pathlib import Path
import pytest
from tabs.function4tabs4.naming import safe_name, join_path


def test_safe_name_and_join_path(tmp_path):
    assert safe_name("curve:1") == "curve_1"
    assert safe_name("") == "untitled"
    path = join_path(tmp_path, "a/b", "c:d")
    assert path == tmp_path / "a_b" / "c_d"


@pytest.mark.parametrize("name", ["Колонна", "Плита", "Стена", "Балка"])
def test_safe_name_cyrillic_words(name):
    assert safe_name(name) == name
