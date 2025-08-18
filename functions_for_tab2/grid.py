"""Grid generation utilities for the second tab.

This module provides helper functions to build grids either uniformly or
from manual user input.  All functions return NumPy arrays and perform
basic validation of the input parameters.
"""

from __future__ import annotations

import numpy as np

from tabs.function_for_all_tabs.parsing_utils import parse_numbers

Array = np.ndarray


def build_grid_uniform(start: float, stop: float, step: float, include_endpoint: bool) -> Array:
    """Generate a uniformly spaced grid.

    Parameters
    ----------
    start, stop, step:
        Parameters of the grid.
    include_endpoint:
        Whether to force the last point to ``stop``.

    Returns
    -------
    numpy.ndarray
        Generated grid of points.

    Raises
    ------
    ValueError
        If ``step`` is zero or the resulting grid would contain fewer than
        two points.
    """

    if step == 0:
        raise ValueError("Шаг не может быть равен нулю")

    n_float = (stop - start) / step
    if include_endpoint:
        n = int(round(n_float)) + 1
    else:
        n = int(np.floor(n_float))
    if n < 2:
        raise ValueError("Количество точек должно быть не менее двух")

    grid = start + step * np.arange(n, dtype=float)
    if include_endpoint:
        grid[-1] = stop
    return grid


def build_grid_manual(text: str) -> Array:
    """Build a grid from manually entered text.

    Parameters
    ----------
    text:
        Text containing numbers separated by whitespace or commas.

    Returns
    -------
    numpy.ndarray
        Array of parsed points.

    Raises
    ------
    ValueError
        If fewer than two points are provided.
    """

    points = parse_numbers(text)
    if points.size < 2:
        raise ValueError("Необходимо минимум две точки")
    return points


__all__ = ["build_grid_uniform", "build_grid_manual"]
