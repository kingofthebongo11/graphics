from unittest.mock import patch

import numpy as np

from tabs.functions_for_tab2 import IntervalSpec
from tabs.functions_for_tab2.segment_builder import build_segment


def test_uniform_const_rounding():
    spec = IntervalSpec(
        id=1,
        primary_axis="X",
        grid_kind="uniform",
        start=0.0,
        stop=2.0,
        step=1.0,
        include_endpoint=True,
        dep_mode="const",
        const_value=1/3,
        precision=2,
    )
    seg = build_segment(spec)
    assert np.allclose(seg.X, [0.0, 1.0, 2.0])
    assert np.allclose(seg.Y, [0.33, 0.33, 0.33])


def test_manual_grid_array_dep():
    spec = IntervalSpec(
        id=2,
        primary_axis="X",
        grid_kind="manual",
        manual_points="0, 1, 2",
        dep_mode="array",
        array_values="3, 4, 5",
    )
    seg = build_segment(spec)
    assert np.allclose(seg.X, [0.0, 1.0, 2.0])
    assert np.allclose(seg.Y, [3.0, 4.0, 5.0])


def test_expr_with_filter_and_y_axis():
    spec = IntervalSpec(
        id=3,
        primary_axis="Y",
        grid_kind="uniform",
        start=0.0,
        stop=2.0,
        step=1.0,
        include_endpoint=True,
        dep_mode="expr",
        expr_text="1/(y-1)",
        precision=2,
        clamp_finite=True,
    )
    seg = build_segment(spec)
    assert np.allclose(seg.X, [-1.0, 1.0])
    assert np.allclose(seg.Y, [0.0, 2.0])


def test_dep_from_file_uses_project_readers(tmp_path):
    dummy = tmp_path / "data.txt"

    def fake_ls(info):
        raise ValueError

    def fake_text(info):
        info["X_values"] = [1.0, 2.0]
        info["Y_values"] = [3.0, 4.0]

    spec = IntervalSpec(
        id=4,
        primary_axis="X",
        dep_mode="from_file",
        dep_file_path=str(dummy),
    )
    with patch("tabs.functions_for_tab2.dependent.read_X_Y_from_ls_dyna", side_effect=fake_ls), \
         patch("tabs.functions_for_tab2.dependent.read_X_Y_from_text_file", side_effect=fake_text):
        seg = build_segment(spec)
    assert np.allclose(seg.X, [1.0, 2.0])
    assert np.allclose(seg.Y, [3.0, 4.0])


def test_manual_pairs_mode():
    spec = IntervalSpec(
        id=5,
        primary_axis="X",
        dep_mode="manual_pairs",
        manual_pairs_text="0 1\n1 2",
    )
    seg = build_segment(spec)
    assert np.allclose(seg.X, [0.0, 1.0])
    assert np.allclose(seg.Y, [1.0, 2.0])


def test_grid_file_pairs(tmp_path):
    dummy = tmp_path / "pairs.txt"

    def fake_ls(info):
        raise ValueError

    def fake_text(info):
        info["X_values"] = [5.0, 6.0]
        info["Y_values"] = [7.0, 8.0]

    spec = IntervalSpec(
        id=6,
        primary_axis="X",
        grid_kind="file_pairs",
        file_pairs_path=str(dummy),
    )
    with patch("tabs.functions_for_tab2.dependent.read_X_Y_from_ls_dyna", side_effect=fake_ls), \
         patch("tabs.functions_for_tab2.dependent.read_X_Y_from_text_file", side_effect=fake_text):
        seg = build_segment(spec)
    assert np.allclose(seg.X, [5.0, 6.0])
    assert np.allclose(seg.Y, [7.0, 8.0])
