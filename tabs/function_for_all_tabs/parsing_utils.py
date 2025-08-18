from __future__ import annotations

from pathlib import Path
import re
from typing import List, Tuple

import numpy as np

from tabs.functions_for_tab1.curves_from_file.text_file import (
    read_X_Y_from_text_file,
)


def read_pairs(path: str) -> Tuple[List[float], List[float]]:
    """Read X and Y value pairs from a text file.

    This function is a thin adapter over
    :func:`tabs.functions_for_tab1.curves_from_file.text_file.read_X_Y_from_text_file`.
    It delegates parsing to the existing implementation and simply returns the
    extracted arrays of X and Y values.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(path)

    curve_info = {"curve_file": str(path_obj)}
    read_X_Y_from_text_file(curve_info)
    try:
        return curve_info["X_values"], curve_info["Y_values"]
    except KeyError as exc:
        raise ValueError("Некорректные данные в файле") from exc


def parse_numbers(text: str) -> np.ndarray:
    """Parse whitespace or comma separated numbers into an array.

    Parameters
    ----------
    text:
        String containing numbers separated by whitespace, commas or
        semicolons.

    Returns
    -------
    numpy.ndarray
        Array of parsed floats.  Empty tokens are ignored.

    Raises
    ------
    ValueError
        If any token cannot be converted to ``float``.
    """

    tokens = re.split(r"[\s,;]+", text.strip())
    numbers: List[float] = []
    for token in tokens:
        if not token:
            continue
        try:
            numbers.append(float(token))
        except ValueError as exc:  # pragma: no cover - defensive branch
            raise ValueError(f"Некорректное число: {token}") from exc
    return np.asarray(numbers, dtype=float)


__all__ = ["read_pairs", "parse_numbers"]
