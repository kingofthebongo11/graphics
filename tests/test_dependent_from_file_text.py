import numpy as np
from pathlib import Path

from tabs.functions_for_tab2.dependent import compute_dependent_values


def test_from_file_with_blank_lines_and_spaces():
    path = Path(__file__).resolve().parents[1] / "examples" / "xy_pairs_with_blanks.txt"
    grid = np.array([0.0])
    x, y = compute_dependent_values(
        "from_file",
        grid,
        arg_name="x",
        const_value=0.0,
        array_values_text="",
        expr_text="",
        dep_file_path=str(path),
        manual_pairs_text="",
    )
    assert np.allclose(x, [1.0, 3.0, 5.0])
    assert np.allclose(y, [2.0, 4.0, 6.0])
