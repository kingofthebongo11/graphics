"""Сохранение и загрузка дерева в формате JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .tree_schema import Tree


def save_tree(tree: Tree, path: str | Path) -> Path:
    """Сохранить ``tree`` в JSON файл ``path``."""
    dest = Path(path)
    dest.write_text(json.dumps(tree.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


def load_tree(path: str | Path) -> Tree:
    """Загрузить дерево из JSON файла."""
    src = Path(path)
    data: Any = json.loads(src.read_text(encoding="utf-8"))
    return Tree.from_dict(data)


__all__ = ["save_tree", "load_tree"]
