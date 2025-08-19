"""Utilities to construct a :class:`ComputedSegment` from :class:`IntervalSpec`."""

from __future__ import annotations

from typing import Tuple

import numpy as np

from function_for_all_tabs.validation import (
    InvalidFormatError,
    SizeMismatchError,
    EmptyDataError,
)
from .models import ComputedSegment, IntervalSpec
from .grid import build_grid_manual, build_grid_uniform
from .dependent import compute_dependent_values

Array = np.ndarray


def _read_pairs(path: str) -> Tuple[Array, Array]:
    """Read ``(x, y)`` pairs from ``path`` using project readers."""
    X, Y = compute_dependent_values(
        "from_file",
        np.array([], dtype=float),
        arg_name="x",
        const_value=0.0,
        array_values_text="",
        expr_text="",
        dep_file_path=path,
        manual_pairs_text="",
    )
    return np.asarray(X, dtype=float), np.asarray(Y, dtype=float)


def _parse_pairs(text: str) -> Tuple[Array, Array]:
    """Parse ``(x, y)`` pairs from a text block using existing utilities."""
    X, Y = compute_dependent_values(
        "manual_pairs",
        np.array([], dtype=float),
        arg_name="x",
        const_value=0.0,
        array_values_text="",
        expr_text="",
        dep_file_path="",
        manual_pairs_text=text,
    )
    return np.asarray(X, dtype=float), np.asarray(Y, dtype=float)


def build_segment(spec: IntervalSpec) -> ComputedSegment:
    """Build a numeric segment according to ``spec``."""
    if spec.grid_kind == "file_pairs":
        X, Y = _read_pairs(spec.file_pairs_path)
    elif spec.dep_mode == "from_file":
        X, Y = _read_pairs(spec.dep_file_path)
    elif spec.dep_mode == "manual_pairs":
        X, Y = _parse_pairs(spec.manual_pairs_text)
    else:
        if spec.grid_kind == "uniform":
            grid = build_grid_uniform(
                spec.start, spec.stop, spec.step, spec.include_endpoint
            )
        elif spec.grid_kind == "manual":
            grid = build_grid_manual(spec.manual_points)
        else:
            raise InvalidFormatError(f"Неизвестный тип сетки: {spec.grid_kind}")

        arg_name = "x" if spec.primary_axis == "X" else "y"
        _, values = compute_dependent_values(
            spec.dep_mode,
            grid,
            arg_name=arg_name,
            const_value=spec.const_value,
            array_values_text=spec.array_values,
            expr_text=spec.expr_text,
            dep_file_path=spec.dep_file_path,
            manual_pairs_text=spec.manual_pairs_text,
        )
        if values is None:
            raise EmptyDataError("Не удалось вычислить зависимые значения")

        if spec.primary_axis == "X":
            X, Y = grid, values
        else:
            X, Y = values, grid

    if X.size != Y.size:
        raise SizeMismatchError("Длины X и Y не совпадают")

    if spec.clamp_finite:
        mask = np.isfinite(X) & np.isfinite(Y)
        X = X[mask]
        Y = Y[mask]

    X = np.round(X, spec.precision)
    Y = np.round(Y, spec.precision)
    return ComputedSegment(X=X, Y=Y)


__all__ = ["build_segment"]

