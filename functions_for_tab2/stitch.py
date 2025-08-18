"""Utilities for stitching computed segments.

This module provides functionality to merge multiple
:class:`~functions_for_tab2.models.ComputedSegment` instances into a
continuous curve.  Optionally, segments can be adjusted to ensure
continuity of the argument axis.
"""

from __future__ import annotations

from typing import List, Literal

import numpy as np

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
        List of segments to be concatenated.
    primary_sequence:
        Sequence indicating which axis acts as the independent variable for
        each segment.  Must be the same length as ``segments``.
    require_continuity:
        When ``True``, the first point of each subsequent segment is adjusted
        to match the last point of the previous segment along its argument
        axis if the values differ by less than ``tol``.
    tol:
        Tolerance for comparing axis values.

    Returns
    -------
    ComputedSegment
        New segment containing the concatenated ``X`` and ``Y`` arrays.
    """

    if not segments:
        return ComputedSegment(X=np.array([], dtype=float), Y=np.array([], dtype=float))

    if len(segments) != len(primary_sequence):
        raise ValueError("Длина primary_sequence должна совпадать с количеством сегментов")

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
