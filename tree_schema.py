from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from analysis_types import ANALYSIS_TYPES

EntityKind = Literal["element", "node"]
ElementType = Literal["beam", "shell", "solid"]


@dataclass
class FileNode:
    """Leaf node that represents a particular element or node."""

    id: int

    def to_dict(self) -> dict:
        return {"id": self.id}

    @classmethod
    def from_dict(cls, data: dict) -> "FileNode":
        return cls(id=int(data["id"]))


@dataclass
class AnalysisNode:
    """Node that groups results by analysis type."""

    analysis_type: str
    children: list[FileNode] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "analysis_type": self.analysis_type,
            "children": [child.to_dict() for child in self.children],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AnalysisNode":
        return cls(
            analysis_type=data["analysis_type"],
            children=[FileNode.from_dict(ch) for ch in data.get("children", [])],
        )


@dataclass
class EntityNode:
    """Top-level node representing an entity (element or node)."""

    user_name: str
    entity_kind: EntityKind
    element_type: ElementType | None = None
    children: list[AnalysisNode] = field(default_factory=list)

    def add_analysis(self, analysis_type: str) -> AnalysisNode:
        """Добавляет подпапку анализа к узлу.

        Parameters
        ----------
        analysis_type: str
            Название анализа, выбранное из ``analysis_types.ANALYSIS_TYPES``.

        Returns
        -------
        AnalysisNode
            Созданный узел анализа.

        Raises
        ------
        ValueError
            Если тип анализа недопустим или уже существует.
        """

        if analysis_type not in ANALYSIS_TYPES:
            raise ValueError("Недопустимый тип анализа")

        if any(ch.analysis_type == analysis_type for ch in self.children):
            raise ValueError("Анализ уже добавлен")

        node = AnalysisNode(analysis_type=analysis_type)
        self.children.append(node)
        return node

    def to_dict(self) -> dict:
        data = {
            "user_name": self.user_name,
            "entity_kind": self.entity_kind,
            "children": [child.to_dict() for child in self.children],
        }
        if self.element_type is not None:
            data["element_type"] = self.element_type
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "EntityNode":
        return cls(
            user_name=data["user_name"],
            entity_kind=data["entity_kind"],
            element_type=data.get("element_type"),
            children=[AnalysisNode.from_dict(ch) for ch in data.get("children", [])],
        )
