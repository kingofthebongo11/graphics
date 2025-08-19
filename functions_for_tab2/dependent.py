"""Utilities for computing dependent coordinate values for tab2."""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional, Tuple

import numpy as np

from function_for_all_tabs.safe_eval import safe_eval_expr
from function_for_all_tabs.validation import (
    InvalidFormatError,
    SizeMismatchError,
)
from tabs.function_for_all_tabs.parsing_utils import parse_numbers
from tabs.functions_for_tab1.curves_from_file import (
    read_X_Y_from_excel,
    read_X_Y_from_ls_dyna,
    read_X_Y_from_text_file,
)

Array = np.ndarray


def _parse_manual_pairs(text: str) -> Tuple[Array, Array]:
    """Parse ``(x, y)`` pairs from a multiline string."""
    xs: list[float] = []
    ys: list[float] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        numbers = parse_numbers(line)
        if numbers.size < 2:
            raise InvalidFormatError(f"Некорректные данные в строке: {line}")
        xs.append(float(numbers[0]))
        ys.append(float(numbers[1]))
    return np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)


def _read_pairs_from_file(path: str) -> Tuple[Array, Array]:
    """Read X and Y arrays from ``path`` using tab1 readers."""
    curve_info = {"curve_file": path}
    suffix = Path(path).suffix.lower()
    if suffix in {".xlsx", ".xlsm", ".csv"}:
        read_X_Y_from_excel(curve_info)
    else:
        try:
            read_X_Y_from_ls_dyna(curve_info)
        except Exception:
            read_X_Y_from_text_file(curve_info)
    return (
        np.asarray(curve_info.get("X_values", []), dtype=float),
        np.asarray(curve_info.get("Y_values", []), dtype=float),
    )


def compute_dependent_values(
    dep_mode: str,
    grid: Array,
    *,
    arg_name: Literal["x", "y"],
    const_value: float,
    array_values_text: str,
    expr_text: str,
    dep_file_path: str,
    manual_pairs_text: str,
) -> Tuple[Optional[Array], Optional[Array]]:
    """Compute dependent coordinate values according to ``dep_mode``."""
    if dep_mode == "const":
        values = np.full_like(grid, const_value, dtype=float)
        return None, values

    if dep_mode == "array":
        values = parse_numbers(array_values_text)
        if values.size != grid.size:
            raise SizeMismatchError("Длины массива и сетки не совпадают")
        return None, values

    if dep_mode == "expr":
        values = safe_eval_expr(expr_text, **{arg_name: grid})
        return None, np.asarray(values, dtype=float)

    if dep_mode == "from_file":
        return _read_pairs_from_file(dep_file_path)

    if dep_mode == "manual_pairs":
        return _parse_manual_pairs(manual_pairs_text)

    raise InvalidFormatError(f"Неизвестный режим: {dep_mode}")


__all__ = ["compute_dependent_values"]

