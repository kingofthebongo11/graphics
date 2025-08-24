from __future__ import annotations

from pathlib import Path
import re
from typing import List, Tuple

import numpy as np

from tabs.function_for_all_tabs.validation import (
    ensure_not_empty,
    InvalidFormatError,
)
from tabs.functions_for_tab1.curves_from_file.text_file import (
    read_X_Y_from_text_file,
)


def read_pairs(path: str) -> Tuple[List[float], List[float]]:
    """Read X and Y value pairs from a text file."""
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(path)
    curve_info = {"curve_file": str(path_obj)}
    read_X_Y_from_text_file(curve_info)
    try:
        return curve_info["X_values"], curve_info["Y_values"]
    except KeyError as exc:
        raise InvalidFormatError("Некорректные данные в файле") from exc


def parse_numbers(text: str) -> np.ndarray:
    """Parse whitespace or comma separated numbers into an array."""
    tokens = re.split(r"[\s,;]+", text.strip())
    numbers: List[float] = []
    for token in tokens:
        if not token:
            continue
        try:
            numbers.append(float(token))
        except ValueError as exc:  # pragma: no cover
            raise InvalidFormatError(f"Некорректное число: {token}") from exc
    ensure_not_empty(numbers, "числа")
    return np.asarray(numbers, dtype=float)


def parse_pairs_text(text: str) -> Tuple[np.ndarray, np.ndarray]:
    """Parse ``(x, y)`` pairs from a multiline string."""
    xs: List[float] = []
    ys: List[float] = []
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


__all__ = ["read_pairs", "parse_numbers", "parse_pairs_text"]

