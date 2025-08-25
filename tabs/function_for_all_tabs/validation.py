"""Проверки и исключения, общие для вкладок."""

from __future__ import annotations


class ValidationError(ValueError):
    """Базовый класс ошибок проверки."""


class EmptyDataError(ValidationError):
    """Отсутствуют требуемые данные."""


class InvalidFormatError(ValidationError):
    """Данные имеют неверный формат."""


class SizeMismatchError(ValidationError):
    """Размеры входных массивов не совпадают."""


class ZeroStepError(ValidationError):
    """Шаг сетки равен нулю."""


class NotEnoughPointsError(ValidationError):
    """Недостаточно точек для операции."""


class InvalidAnalysisTypeError(ValidationError):
    """Недопустимый тип анализа."""


def ensure_not_empty(seq, name: str = "данные"):
    """Гарантирует, что последовательность не пуста."""
    if not seq:
        raise EmptyDataError(f"{name.capitalize()} отсутствуют")
    return seq


def ensure_numbers(seq, name: str = "значения"):
    """Преобразует элементы в ``float`` и проверяет формат."""
    try:
        return [float(v) for v in seq]
    except (TypeError, ValueError) as exc:
        raise InvalidFormatError(f"{name.capitalize()} должны быть числами") from exc


def ensure_same_length(a, b, name_a: str = "X", name_b: str = "Y"):
    """Проверяет равенство длины двух последовательностей."""
    if len(a) != len(b):
        raise SizeMismatchError(f"{name_a} и {name_b} разной длины")
    return a, b


def ensure_non_zero_step(step: float):
    """Проверяет, что шаг не равен нулю."""
    if step == 0:
        raise ZeroStepError("Шаг не может быть нулевым")
    return step


def ensure_min_length(data, min_len: int = 2, name: str = "точек"):
    """Проверяет минимальное количество элементов."""
    length = data if isinstance(data, int) else len(data)
    if length < min_len:
        raise NotEnoughPointsError(f"Нужно минимум {min_len} {name}")
    return data


def ensure_analysis_type(analysis_type: str):
    """Проверяет, что тип анализа поддерживается."""
    from analysis_types import ANALYSIS_TYPES  # локальный импорт для избежания циклов

    if analysis_type not in ANALYSIS_TYPES:
        raise InvalidAnalysisTypeError("Некорректный тип анализа")
    return analysis_type


__all__ = [
    "ValidationError",
    "EmptyDataError",
    "InvalidFormatError",
    "SizeMismatchError",
    "ZeroStepError",
    "NotEnoughPointsError",
    "InvalidAnalysisTypeError",
    "ensure_not_empty",
    "ensure_numbers",
    "ensure_same_length",
    "ensure_non_zero_step",
    "ensure_min_length",
    "ensure_analysis_type",
]
