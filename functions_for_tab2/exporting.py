"""Функции экспорта рассчитанных кривых."""

from __future__ import annotations

import numpy as np

from function_for_all_tabs.validation import (
    ensure_same_length,
    ensure_min_length,
)

Array = np.ndarray


def export_curve_txt(path: str, X: Array, Y: Array, precision: int) -> None:
    """Сохранить кривую в текстовый файл."""
    x = np.asarray(X).ravel()
    y = np.asarray(Y).ravel()
    ensure_same_length(x, y, "X", "Y")
    ensure_min_length(x, min_len=1, name="точек")
    fmt = f"{{:.{precision}f}} {{:.{precision}f}}\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"{x.size}\n")
        for xv, yv in zip(x, y):
            fh.write(fmt.format(xv, yv))


__all__ = ["export_curve_txt"]

