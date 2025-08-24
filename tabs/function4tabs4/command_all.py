"""Сбор команд для всего дерева анализа."""

from __future__ import annotations

from typing import List

from .command_single import build_command
from .tree_schema import Tree


def collect_commands(tree: Tree) -> List[str]:
    """Сгенерировать команды для всех кривых в дереве."""
    commands: List[str] = []
    for analysis in tree.analyses:
        for curve in analysis.curves:
            commands.append(build_command(curve.name, curve.props))
    return commands


__all__ = ["collect_commands"]
