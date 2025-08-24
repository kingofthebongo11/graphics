from pathlib import Path
from unittest.mock import patch

import pytest

from tabs.functions_for_tab1.curves_from_file.ls_dyna_file import read_X_Y_from_ls_dyna


def test_ls_dyna_invalid_file():
    file_path = Path(__file__).resolve().parents[1] / 'examples' / 'Text' / 'exampletext.txt'
    curve_info = {'curve_file': str(file_path)}
    with patch('tabs.functions_for_tab1.curves_from_file.ls_dyna_file.messagebox.showerror'):
        with pytest.raises(ValueError):
            read_X_Y_from_ls_dyna(curve_info)
    assert 'X_values' not in curve_info
    assert 'Y_values' not in curve_info
