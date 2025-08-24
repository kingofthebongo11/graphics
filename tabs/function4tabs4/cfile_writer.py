"""Запись набора команд в файл ``.cfile``."""

from __future__ import annotations

from pathlib import Path

from .command_all import collect_commands
from .tree_schema import Tree


def write_cfile(tree: Tree, path: str | Path) -> Path:
    """Записать команды из ``tree`` в файл ``path``."""
    commands = collect_commands(tree)
    dest = Path(path)
    dest.write_text("\n".join(commands) + "\n", encoding="utf-8")
    return dest


__all__ = ["write_cfile"]
