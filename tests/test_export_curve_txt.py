import re

import numpy as np
import pytest

from functions_for_tab2.exporting import export_curve_txt


def test_export_curve_txt_structure(tmp_path):
    x = np.array([0.123456, 1.234567])
    y = np.array([2.345678, 3.456789])
    path = tmp_path / "curve.txt"

    export_curve_txt(str(path), x, y, precision=3)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "2"
    assert len(lines) == 3
    pattern = re.compile(r"-?\d+\.\d{3} -?\d+\.\d{3}")
    assert pattern.fullmatch(lines[1])
    assert pattern.fullmatch(lines[2])


def test_export_curve_txt_validation(tmp_path):
    path = tmp_path / "curve.txt"

    with pytest.raises(ValueError):
        export_curve_txt(str(path), np.array([1.0]), np.array([]), precision=2)

    with pytest.raises(ValueError):
        export_curve_txt(str(path), np.array([]), np.array([]), precision=2)
