from naming import safe_name, make_curve_path


def test_safe_name_keeps_cyrillic_and_spaces():
    name = "Пример Имя"
    assert safe_name(name) == name


def test_safe_name_removes_invalid_characters():
    name = 'te<st>:"na/me\\?*'
    assert safe_name(name) == 'testname'


def test_make_curve_path(tmp_path):
    base = tmp_path
    path = make_curve_path(base, 'ТОП', 'анализ', 'ID:1', '.txt')
    expected = base / 'curves' / 'ТОП' / 'анализ' / 'ID1.txt'
    assert path == expected
    assert not path.parent.exists()
