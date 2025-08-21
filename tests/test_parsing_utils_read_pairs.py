import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from tabs.function_for_all_tabs.parsing_utils import read_pairs


def test_read_pairs_valid_file():
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as tmp:
        tmp.write('1 2\n3,4\n\n5 6\n')
        path = tmp.name

    x, y = read_pairs(path)
    assert x == [1.0, 3.0, 5.0]
    assert y == [2.0, 4.0, 6.0]
    Path(path).unlink()


def test_read_pairs_invalid_line():
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as tmp:
        tmp.write('1 2\ninvalid\n')
        path = tmp.name

    with patch('tabs.functions_for_tab1.curves_from_file.text_file.messagebox.showerror'), \
            pytest.raises(ValueError):
        read_pairs(path)
    Path(path).unlink()


def test_read_pairs_missing_file():
    missing = Path('nonexistent_file.txt')
    with pytest.raises(FileNotFoundError):
        read_pairs(missing)
