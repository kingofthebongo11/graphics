"""Utilities for computing dependent coordinate values for tab2."""

from __future__ import annotations

from typing import Literal, Optional, Tuple

import numpy as np

from tabs.function_for_all_tabs.safe_eval import safe_eval_expr
from tabs.function_for_all_tabs.validation import (
    InvalidFormatError,
    SizeMismatchError,
)
from tabs.function_for_all_tabs.parsing_utils import parse_numbers
from tabs.function_for_all_tabs import parse_pairs_text, read_pairs_any
from tabs.functions_for_tab1.curves_from_file import (
    read_X_Y_from_excel,
    read_X_Y_from_ls_dyna,
    read_X_Y_from_text_file,
)

Array = np.ndarray



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
        xs, ys = read_pairs_any(
            dep_file_path,
            read_excel=read_X_Y_from_excel,
            read_ls_dyna=read_X_Y_from_ls_dyna,
            read_text=read_X_Y_from_text_file,
        )
        return np.asarray(xs, dtype=float), np.asarray(ys, dtype=float)

    if dep_mode == "manual_pairs":
        return parse_pairs_text(manual_pairs_text)

    raise InvalidFormatError(f"Неизвестный режим: {dep_mode}")


__all__ = ["compute_dependent_values"]

