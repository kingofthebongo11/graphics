from pathlib import Path

from tabs.functions_for_tab1.curves_from_file.ls_dyna_file import read_X_Y_from_ls_dyna


def test_ls_dyna_example_with_header():
    file_path = Path(__file__).resolve().parents[1] / 'examples' / 'LsDynaText' / 'LsDyna_example.txt'
    curve_info = {'curve_file': str(file_path)}
    read_X_Y_from_ls_dyna(curve_info)
    assert curve_info['X_values'][:3] == [0.0, 9.9993146956e-02, 1.9999520481e-01]
    assert curve_info['Y_values'][:3] == [0.0, 7.6113149524e-02, 8.0158777535e-02]
