import tempfile
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tabs.functions_for_tab1.curves_from_file.combined_curve import read_X_Y_from_combined


def _create_temp_file(content: str):
    tmp = tempfile.NamedTemporaryFile('w+', delete=False)
    tmp.write(content)
    tmp.flush()
    return tmp


def test_text_file_column_selection():
    tmp = _create_temp_file('1 10\n2 20\n3 30\n')
    curve_info = {
        'X_source': {
            'source': 'Текстовой файл',
            'curve_file': tmp.name,
            'column': 1,
        },
        'Y_source': {
            'source': 'Текстовой файл',
            'curve_file': tmp.name,
            'column': 0,
        },
    }
    read_X_Y_from_combined(curve_info)
    assert curve_info['X_values'] == [10.0, 20.0, 30.0]
    assert curve_info['Y_values'] == [1.0, 2.0, 3.0]


def test_lsdyna_file_column_selection():
    tmp = _create_temp_file('1 10\n2 20\n3 30\n')
    curve_info = {
        'X_source': {
            'source': 'Файл кривой LS-Dyna',
            'curve_file': tmp.name,
            'column': 1,
        },
        'Y_source': {
            'source': 'Файл кривой LS-Dyna',
            'curve_file': tmp.name,
            'column': 0,
        },
    }
    read_X_Y_from_combined(curve_info)
    assert curve_info['X_values'] == [10.0, 20.0, 30.0]
    assert curve_info['Y_values'] == [1.0, 2.0, 3.0]
