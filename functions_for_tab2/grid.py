"""Grid generation utilities for the second tab."""

from __future__ import annotations

import numpy as np

from function_for_all_tabs.validation import (
    ensure_non_zero_step,
    ensure_min_length,
)
from tabs.function_for_all_tabs.parsing_utils import parse_numbers

Array = np.ndarray


def build_grid_uniform(start: float, stop: float, step: float, include_endpoint: bool) -> Array:
    """Generate a uniformly spaced grid."""
    ensure_non_zero_step(step)
    n_float = (stop - start) / step
    if include_endpoint:
        n = int(round(n_float)) + 1
    else:
        n = int(np.floor(n_float))
    ensure_min_length(n)
    grid = start + step * np.arange(n, dtype=float)
    if include_endpoint:
        grid[-1] = stop
    return grid


def build_grid_manual(text: str) -> Array:
    """Build a grid from manually entered text."""
    points = parse_numbers(text)
    ensure_min_length(points, name="точек")
    return points


__all__ = ["build_grid_uniform", "build_grid_manual"]

