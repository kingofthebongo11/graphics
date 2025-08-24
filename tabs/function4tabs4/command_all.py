"""Сбор команд для всего дерева анализа."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .command_single import build_command, build_curve_commands
from .tree_schema import Tree
from topfolder_codec import encode_topfolder
from tree_schema import EntityNode


def walk_tree_and_build_commands(
    root: Iterable[EntityNode],
    base_project_dir: Path | str,
    curves_dirname: str = "curves",
) -> List[str]:
    """Обойти дерево и построить команды для всех кривых."""
    commands: List[str] = []
    base_dir = Path(base_project_dir)

    # --- Перебор верхних узлов ---
    for node in root:
        top_folder_name = encode_topfolder(
            node.user_name, node.entity_kind, node.element_type
        )

        # --- Перебор анализов ---
        for analysis in node.children:

            # --- Перебор файлов ---
            for file_node in analysis.children:
                commands.extend(
                    build_curve_commands(
                        str(base_dir),
                        top_folder_name,
                        analysis.analysis_type,
                        node.entity_kind,
                        node.element_type,
                        file_node.id,
                        curves_dirname,
                    )
                )

    return commands


def collect_commands(tree: Tree) -> List[str]:
    """Сгенерировать команды для всех кривых в дереве."""
    commands: List[str] = []
    for analysis in tree.analyses:
        for curve in analysis.curves:
            commands.append(build_command(curve.name, curve.props))
    return commands


__all__ = ["collect_commands", "walk_tree_and_build_commands"]
