"""Сбор команд для всего дерева анализа."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Mapping, Sequence

from .command_single import build_command, build_curve_commands
from .tree_schema import Tree
from topfolder_codec import encode_topfolder
from tree_schema import EntityNode


def walk_tree_and_build_commands(
    root: Iterable[EntityNode],
    base_project_dir: Path | str,
    curves_dirname: str = "curves",
    top_folder_names: Sequence[str] | None = None,
    analysis_name_maps: Sequence[Mapping[str, str]] | None = None,
) -> List[str]:
    """Обойти дерево и построить команды для всех кривых."""
    commands: List[str] = []
    base_dir = Path(base_project_dir)

    nodes = list(root)
    if top_folder_names is None:
        names = [
            encode_topfolder(n.user_name, n.entity_kind, n.element_type) for n in nodes
        ]
    else:
        names = list(top_folder_names)

    if analysis_name_maps is None:
        analysis_name_maps = [{} for _ in nodes]
    else:
        analysis_name_maps = list(analysis_name_maps)
        if len(analysis_name_maps) < len(nodes):
            analysis_name_maps.extend({} for _ in range(len(nodes) - len(analysis_name_maps)))

    for node, top_folder_name, analysis_map in zip(nodes, names, analysis_name_maps):

        for analysis in node.children:
            numbered_analysis = analysis_map.get(
                analysis.analysis_type, analysis.analysis_type
            )
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
                        numbered_analysis,
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
