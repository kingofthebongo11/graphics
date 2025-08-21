"""Утилиты, общие для всех вкладок."""

from .plotting import create_plot
from .parsing_utils import read_pairs, parse_numbers
from .plotting_adapter import create_plot_canvas, plot_on_canvas
from .readers import read_pairs_any
from .safe_eval import safe_eval_expr
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
    "create_plot",
    "read_pairs",
    "parse_numbers",
    "create_plot_canvas",
    "plot_on_canvas",
    "read_pairs_any",
    "safe_eval_expr",
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

