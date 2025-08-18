"""Data models for tab2 computations.

This module defines lightweight dataclasses used by the second tab of the
application.  They are independent from any GUI code and contain no side
effects on import.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Literal

import numpy as np


@dataclass
class IntervalSpec:
    """Specification of a computation interval.

    Attributes
    ----------
    id:
        Internal identifier of the interval.
    primary_axis:
        Which axis values should be treated as independent: ``"X"`` or ``"Y"``.
    grid_kind:
        How grid points are supplied: ``"uniform"``, ``"manual``" or
        ``"file_pairs"``.
    start, stop, step:
        Parameters for uniform grid generation.
    include_endpoint:
        Whether to include ``stop`` as the last grid point.
    manual_points:
        Text with newline-separated grid points for ``manual`` grid.
    file_pairs_path:
        Path to file with ``(x, y)`` pairs when ``grid_kind`` is
        ``"file_pairs"``.
    dep_mode:
        Mode for defining dependent variable: ``"const"``, ``"array"``,
        ``"expr"``, ``"from_file"`` or ``"manual_pairs"``.
    const_value, array_values, expr_text, dep_file_path, manual_pairs_text:
        Parameters for various ``dep_mode`` values.
    precision:
        Number of decimal places to keep when exporting values.
    clamp_finite:
        Whether to clamp ``nan`` and ``inf`` values to finite numbers.
    """

    id: int
    primary_axis: Literal["X", "Y"]

    # Grid specification
    grid_kind: Literal["uniform", "manual", "file_pairs"] = "uniform"
    start: float = 0.0
    stop: float = 1.0
    step: float = 1.0
    include_endpoint: bool = True
    manual_points: str = ""
    file_pairs_path: str = ""

    # Dependent variable specification
    dep_mode: Literal[
        "const", "array", "expr", "from_file", "manual_pairs"
    ] = "const"
    const_value: float = 0.0
    array_values: str = ""
    expr_text: str = ""
    dep_file_path: str = ""
    manual_pairs_text: str = ""

    # Export options
    precision: int = 6
    clamp_finite: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the specification to a plain dictionary."""

        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IntervalSpec":
        """Create :class:`IntervalSpec` from a dictionary."""

        return cls(**data)


@dataclass
class ComputedSegment:
    """Result of computations for a single segment."""

    X: np.ndarray
    Y: np.ndarray

    def to_dict(self) -> Dict[str, Any]:
        """Represent the segment as a dictionary of Python lists."""

        return {"X": self.X.tolist(), "Y": self.Y.tolist()}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ComputedSegment":
        """Create :class:`ComputedSegment` from dictionary data."""

        x = np.asarray(data.get("X", []), dtype=float)
        y = np.asarray(data.get("Y", []), dtype=float)
        return cls(X=x, Y=y)


__all__ = ["IntervalSpec", "ComputedSegment"]
