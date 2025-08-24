from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

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
