from pathlib import Path

from tabs.functions_for_tab1.curves_from_file.ls_dyna_file import read_X_Y_from_ls_dyna


def test_ls_dyna_example_without_markers():
    file_path = (
        Path(__file__).resolve().parents[1]
        / 'examples'
        / 'LsDynaText'
        / 'LsDyna_example2.txt'
    )
    curve_info = {'curve_file': str(file_path)}
    read_X_Y_from_ls_dyna(curve_info)
    assert curve_info['X_values'] == [0.0, 1.0, 2.0, 3.0, 4.0]
    assert curve_info['Y_values'] == [0.0, 1.0, 4.0, 9.0, 16.0]
