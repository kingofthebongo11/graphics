from __future__ import annotations

"""Шаблоны интервалов для второй вкладки."""

import math
from typing import Callable, Dict

from .models import IntervalSpec


def sine(interval_id: int) -> IntervalSpec:
    """Интервал с синусом ``sin(x)`` на ``[0, 2π]``."""
    return IntervalSpec(
        id=interval_id,
        primary_axis="X",
        grid_kind="uniform",
        start=0.0,
        stop=2 * math.pi,
        step=0.1,
        include_endpoint=True,
        dep_mode="expr",
        expr_text="sin(x)",
    )


def parabola(interval_id: int) -> IntervalSpec:
    """Интервал для параболы ``y = x**2`` на ``[-5, 5]``."""
    return IntervalSpec(
        id=interval_id,
        primary_axis="X",
        grid_kind="uniform",
        start=-5.0,
        stop=5.0,
        step=0.5,
        include_endpoint=True,
        dep_mode="expr",
        expr_text="x**2",
    )


def step(interval_id: int) -> IntervalSpec:
    """Интервал для ступенчатой функции ``x >= 0`` на ``[-1, 1]``."""
    return IntervalSpec(
        id=interval_id,
        primary_axis="X",
        grid_kind="uniform",
        start=-1.0,
        stop=1.0,
        step=0.1,
        include_endpoint=True,
        dep_mode="expr",
        expr_text="x >= 0",
    )


PRESETS: Dict[str, Callable[[int], IntervalSpec]] = {
    "Синус": sine,
    "Парабола": parabola,
    "Ступенька": step,
}

__all__ = ["PRESETS", "sine", "parabola", "step"]
