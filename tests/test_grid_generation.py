import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from functions_for_tab2.grid import build_grid_manual, build_grid_uniform


def test_uniform_includes_endpoint():
    grid = build_grid_uniform(0.0, 4.0, 0.5, True)
    assert grid[-1] == pytest.approx(4.0)


def test_uniform_small_range_error():
    with pytest.raises(ValueError):
        build_grid_uniform(0.0, 0.2, 1.0, True)


def test_uniform_negative_step():
    grid = build_grid_uniform(1.0, 0.0, -0.5, True)
    assert np.allclose(grid, [1.0, 0.5, 0.0])


def test_uniform_rounding_boundary():
    grid = build_grid_uniform(0.0, 1.0, 0.1, True)
    assert grid[-1] == pytest.approx(1.0)
    assert len(grid) == 11


def test_manual_too_few_points():
    with pytest.raises(ValueError):
        build_grid_manual("1")
