"""Concatenate multiple segments into a continuous curve.

Функция склеивает несколько отдельных сегментов в одну непрерывную
кривую.  При необходимости она выравнивает первую точку следующего
сегмента по последней точке текущего сегмента, если их значения по
соответствующей оси аргумента совпадают с заданной точностью.
"""

from __future__ import annotations

from typing import List, Literal

import numpy as np

from tabs.function_for_all_tabs.validation import SizeMismatchError
from .models import ComputedSegment

Array = np.ndarray


def stitch_segments(
    segments: List[ComputedSegment],
    primary_sequence: List[Literal["X", "Y"]],
    require_continuity: bool,
    tol: float = 1e-8,
) -> ComputedSegment:
    """Concatenate segments into a single curve.

    Parameters
    ----------
    segments:
        Список сегментов, каждый из которых содержит массивы ``X`` и ``Y``.
    primary_sequence:
        Последовательность осей аргумента, используемых при построении
        соответствующих сегментов (``"X"`` или ``"Y"``).
    require_continuity:
        Если ``True``, первая точка очередного сегмента будет приведена к
        последней точке предыдущего по оси аргумента. Если разница по этой
        оси меньше ``tol`` и обе координаты совпадают по значению, то
        дублирующая точка исключается.
    tol:
        Допустимое расхождение между соседними сегментами. Значение по
        умолчанию ``1e-8`` подобрано так, чтобы игнорировать накопленные
        ошибки округления при вычислениях в числах двойной точности.

    Returns
    -------
    ComputedSegment
        Склеенный сегмент.
    """
    if not segments:
        return ComputedSegment(X=np.array([], dtype=float), Y=np.array([], dtype=float))
    if len(segments) != len(primary_sequence):
        raise SizeMismatchError("Несовпадение числа сегментов и осей")

    xs = [segments[0].X.copy()]
    ys = [segments[0].Y.copy()]
    last_x = xs[0][-1]
    last_y = ys[0][-1]

    for seg, primary in zip(segments[1:], primary_sequence[1:]):
        X = seg.X.copy()
        Y = seg.Y.copy()
        if require_continuity:
            if primary == "X" and abs(X[0] - last_x) <= tol:
                X[0] = last_x
            elif primary == "Y" and abs(Y[0] - last_y) <= tol:
                Y[0] = last_y
        is_duplicate = abs(X[0] - last_x) <= tol and abs(Y[0] - last_y) <= tol
        if not require_continuity:
            eps = np.finfo(float).eps
            is_duplicate = abs(X[0] - last_x) <= eps and abs(Y[0] - last_y) <= eps
        if is_duplicate:
            xs.append(X[1:])
            ys.append(Y[1:])
        else:
            xs.append(X)
            ys.append(Y)
        last_x = X[-1]
        last_y = Y[-1]

    return ComputedSegment(X=np.concatenate(xs), Y=np.concatenate(ys))


__all__ = ["stitch_segments"]

