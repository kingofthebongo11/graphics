import tempfile
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1]))
from tabs.functions_for_tab1.curves_from_file.text_file import read_X_Y_from_text_file


def test_text_file_invalid_extension():
    with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False) as tmp:
        tmp.write('1,2\n3,4\n')
        tmp_path = tmp.name

    curve_info = {'curve_file': tmp_path}
    with patch('tabs.functions_for_tab1.curves_from_file.text_file.messagebox.showerror'):
        read_X_Y_from_text_file(curve_info)
    assert 'X_values' not in curve_info
    assert 'Y_values' not in curve_info
