"""Сохранение и загрузка дерева в формате JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, List

from tree_schema import EntityNode


def save_tree(tree: Iterable[EntityNode], path: str | Path) -> Path:
    """Сохранить ``tree`` в JSON файл ``path``."""
    dest = Path(path)
    data = [node.to_dict() for node in tree]
    dest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest


def load_tree(path: str | Path) -> List[EntityNode]:
    """Загрузить дерево из JSON файла."""
    src = Path(path)
    data: Any = json.loads(src.read_text(encoding="utf-8"))
    nodes = [EntityNode.from_dict(d) for d in data]
    for node in nodes:  # Пересчитываем имя папки верхнего уровня
        node.recalc_top_folder_name()
    return nodes


__all__ = ["save_tree", "load_tree"]
