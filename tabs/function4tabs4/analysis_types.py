"""Реестр типов анализа и соответствующих подпапок."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class AnalysisType:
    """Описание типа анализа."""

    name: str
    folder: str


_ANALYSIS_TYPES: Dict[str, AnalysisType] = {}


def register_analysis_type(name: str, folder: str) -> None:
    """Зарегистрировать новый тип анализа."""
    _ANALYSIS_TYPES[name] = AnalysisType(name=name, folder=folder)


def get_analysis_type(name: str) -> AnalysisType:
    """Получить описание типа анализа по имени."""
    return _ANALYSIS_TYPES[name]


# Тип анализа по умолчанию
register_analysis_type("default", "analysis")


__all__ = ["AnalysisType", "register_analysis_type", "get_analysis_type"]
