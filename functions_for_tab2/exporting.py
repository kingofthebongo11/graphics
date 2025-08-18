"""Utilities for exporting computed curves to text files."""

from __future__ import annotations

import numpy as np

Array = np.ndarray


def export_curve_txt(path: str, X: Array, Y: Array, precision: int) -> None:
    """Сохранить кривую в текстовый файл в специальном формате.

    Параметры
    ----------
    path:
        Путь к выходному файлу.
    X, Y:
        Массивы значений осей.
    precision:
        Количество знаков после запятой при записи.

    Исключения
    ----------
    ValueError
        Если размеры ``X`` и ``Y`` различаются или нет точек.
    """
    x = np.asarray(X).ravel()
    y = np.asarray(Y).ravel()
    if x.shape != y.shape:
        raise ValueError("X и Y должны иметь одинаковую длину")
    n = x.size
    if n == 0:
        raise ValueError("Количество точек должно быть положительным")

    fmt = f"{{:.{precision}f}} {{:.{precision}f}}\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"{n}\n")
        for xv, yv in zip(x, y):
            fh.write(fmt.format(xv, yv))


__all__ = ["export_curve_txt"]
