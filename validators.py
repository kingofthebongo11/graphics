"""Проверки структур входных данных для анализа."""
from __future__ import annotations
from typing import Iterable

class ValidationError(ValueError):
    """Ошибка проверки входных данных."""


ALLOWED_ANALYSIS_TYPES = {"static", "dynamic", "frequency"}


def ensure_unique_names(items: Iterable, key: str = "name"):
    """Проверяет, что имена объектов на одном уровне уникальны."""
    names = [getattr(item, key, item.get(key) if isinstance(item, dict) else None) for item in items]
    if None in names:
        raise ValidationError("Объекты должны содержать поле имени")
    if len(names) != len(set(names)):
        raise ValidationError("Имена должны быть уникальны на одном уровне")
    return items


def validate_entity(data: dict):
    """Проверяет корректность описания сущности."""
    kind = data.get("entity_kind")
    if kind not in {"element", "node"}:
        raise ValidationError("entity_kind может быть только 'element' или 'node'")
    if kind == "element" and not data.get("element_type"):
        raise ValidationError("Для 'element' необходимо указать element_type")
    return data


def validate_filename(name: str):
    """Имя файла должно состоять только из цифр."""
    if not name.isdigit():
        raise ValidationError("Имя файла должно содержать только цифры")
    return name


def validate_analysis_type(analysis_type: str):
    """Проверяет тип анализа по реестру допустимых значений."""
    if analysis_type not in ALLOWED_ANALYSIS_TYPES:
        raise ValidationError("Недопустимый тип анализа")
    return analysis_type


__all__ = [
    "ValidationError",
    "ALLOWED_ANALYSIS_TYPES",
    "ensure_unique_names",
    "validate_entity",
    "validate_filename",
    "validate_analysis_type",
]
