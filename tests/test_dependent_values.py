from unittest.mock import patch

import numpy as np
import pytest

from functions_for_tab2.dependent import compute_dependent_values


def test_const_mode():
    grid = np.array([0.0, 1.0, 2.0])
    x, vals = compute_dependent_values(
        "const", grid, arg_name="x", const_value=2.5,
        array_values_text="", expr_text="", dep_file_path="", manual_pairs_text=""
    )
    assert x is None
    assert np.allclose(vals, [2.5, 2.5, 2.5])


def test_array_mode():
    grid = np.array([0.0, 1.0, 2.0])
    x, vals = compute_dependent_values(
        "array", grid, arg_name="x", const_value=0.0,
        array_values_text="1, 2, 3", expr_text="", dep_file_path="", manual_pairs_text=""
    )
    assert x is None
    assert np.allclose(vals, [1.0, 2.0, 3.0])

    with pytest.raises(ValueError):
        compute_dependent_values(
            "array", grid, arg_name="x", const_value=0.0,
            array_values_text="1, 2", expr_text="", dep_file_path="", manual_pairs_text=""
        )


def test_expr_mode():
    grid = np.array([0.0, 1.0, 2.0])
    x, vals = compute_dependent_values(
        "expr", grid, arg_name="x", const_value=0.0,
        array_values_text="", expr_text="x*2", dep_file_path="", manual_pairs_text=""
    )
    assert x is None
    assert np.allclose(vals, [0.0, 2.0, 4.0])


def test_from_file_uses_tab1_reader(tmp_path):
    grid = np.array([0.0])
    dummy_path = tmp_path / "data.txt"

    def fake_ls_dyna(info):
        raise ValueError

    def fake_text(info):
        info["X_values"] = [1.0, 2.0]
        info["Y_values"] = [3.0, 4.0]

    with patch("functions_for_tab2.dependent.read_X_Y_from_ls_dyna", side_effect=fake_ls_dyna), \
         patch("functions_for_tab2.dependent.read_X_Y_from_text_file", side_effect=fake_text) as mock_text:
        X, Y = compute_dependent_values(
            "from_file", grid, arg_name="x", const_value=0.0,
            array_values_text="", expr_text="", dep_file_path=str(dummy_path), manual_pairs_text=""
        )
    assert mock_text.called
    assert np.allclose(X, [1.0, 2.0])
    assert np.allclose(Y, [3.0, 4.0])
