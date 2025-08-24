"""Структуры данных для дерева анализа.

В модуле определены простые модели узлов дерева и связанные
константы, используемые четвёртой вкладкой приложения.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

# Имя папки по умолчанию, содержащей результаты анализа
DEFAULT_TOPFOLDER = "Curves"


@dataclass
class CurveNode:
    """Информация об одной кривой."""

    name: str
    path: str
    props: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать узел в словарь."""
        return {"name": self.name, "path": self.path, "props": dict(self.props)}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CurveNode":
        """Создать узел кривой из словаря."""
        return cls(name=data.get("name", ""), path=data.get("path", ""), props=dict(data.get("props", {})))


@dataclass
class AnalysisFolder:
    """Папка с кривыми одного типа анализа."""

    name: str
    curves: List[CurveNode] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "curves": [c.to_dict() for c in self.curves]}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnalysisFolder":
        curves = [CurveNode.from_dict(c) for c in data.get("curves", [])]
        return cls(name=data.get("name", ""), curves=curves)


@dataclass
class Tree:
    """Корневой объект дерева анализа."""

    top: str = DEFAULT_TOPFOLDER
    analyses: List[AnalysisFolder] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"top": self.top, "analyses": [a.to_dict() for a in self.analyses]}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tree":
        analyses = [AnalysisFolder.from_dict(a) for a in data.get("analyses", [])]
        return cls(top=data.get("top", DEFAULT_TOPFOLDER), analyses=analyses)


__all__ = ["DEFAULT_TOPFOLDER", "CurveNode", "AnalysisFolder", "Tree"]
