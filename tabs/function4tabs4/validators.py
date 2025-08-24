"""Проверка имён и свойств узлов дерева."""

from __future__ import annotations

import re
from typing import Any, Dict, Iterable

from tabs.function_for_all_tabs.validation import ValidationError

_NAME_RE = re.compile(r"^[A-Za-z0-9 _\-]+$")


def validate_name(name: str) -> str:
    """Убедиться, что имя не пустое и содержит допустимые символы."""
    if not name:
        raise ValidationError("Имя не может быть пустым")
    if not _NAME_RE.match(name):
        raise ValidationError("Недопустимые символы в имени")
    return name


def validate_properties(props: Dict[str, Any], required: Iterable[str] = ()) -> Dict[str, Any]:
    """Проверить наличие обязательных свойств."""
    for key in required:
        if key not in props:
            raise ValidationError(f"Отсутствует обязательное свойство: {key}")
    return props


__all__ = ["validate_name", "validate_properties"]
