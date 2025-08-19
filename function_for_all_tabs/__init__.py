"""Utilities shared across application tabs."""

from .safe_eval import safe_eval_expr
from .plotting_adapter import create_plot_canvas, plot_on_canvas
from .validation import (
    ValidationError,
    EmptyDataError,
    InvalidFormatError,
    SizeMismatchError,
    ZeroStepError,
    NotEnoughPointsError,
    ensure_not_empty,
    ensure_numbers,
    ensure_same_length,
    ensure_non_zero_step,
    ensure_min_length,
)

__all__ = [
    "safe_eval_expr",
    "create_plot_canvas",
    "plot_on_canvas",
    "ValidationError",
    "EmptyDataError",
    "InvalidFormatError",
    "SizeMismatchError",
    "ZeroStepError",
    "NotEnoughPointsError",
    "ensure_not_empty",
    "ensure_numbers",
    "ensure_same_length",
    "ensure_non_zero_step",
    "ensure_min_length",
]
