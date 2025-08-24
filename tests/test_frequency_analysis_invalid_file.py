import tempfile
from unittest.mock import patch

import pytest

from tabs.functions_for_tab1.curves_from_file.frequency_analysis import (
    read_X_Y_from_frequency_analysis,
)


def _curve_info(path: str):
    return {
        'curve_file': path,
        'curve_typeXF': 'Время',
        'curve_typeYF': 'Частота',
        'curve_typeXF_type': 'X',
        'curve_typeYF_type': 'X',
    }


def test_frequency_analysis_invalid_extension():
    with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False) as tmp:
        tmp.write('data')
        tmp_path = tmp.name
    curve_info = _curve_info(tmp_path)
    with patch('tabs.functions_for_tab1.curves_from_file.frequency_analysis.messagebox.showerror'):
        read_X_Y_from_frequency_analysis(curve_info)
    assert 'X_values' not in curve_info
    assert 'Y_values' not in curve_info


def test_frequency_analysis_missing_header():
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as tmp:
        tmp.write('no headers here\n')
        tmp_path = tmp.name
    curve_info = _curve_info(tmp_path)
    with patch('tabs.functions_for_tab1.curves_from_file.frequency_analysis.messagebox.showerror'):
        with pytest.raises(ValueError):
            read_X_Y_from_frequency_analysis(curve_info)
    assert 'X_values' not in curve_info
    assert 'Y_values' not in curve_info
