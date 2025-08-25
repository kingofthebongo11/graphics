"""Генерация команды для одной кривой."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple
from pathlib import PureWindowsPath

from analysis_types import ANALYSIS_TYPE_CODES
from .naming import safe_name


ETYPE_BY_ELEMENT: Dict[str, int] = {
    "beam": 1,
    "shell": 2,
    "solid": 3,
}

# Шаблоны выбора сущности в LS-PrePost.
# Ключем служит кортеж (entity_kind, element_type).
SELECT_TEMPLATES: Dict[Tuple[str, str | None], List[str]] = {
    ("element", "beam"): [
        "genselect clear all",
        "genselect target beam",
        "genselect beam add beam {element_id}/0",
        "etype {etype} ;etime {etime}",
    ],
    ("element", "shell"): [
        "genselect clear all",
        "genselect target shell",
        "genselect shell add shell {element_id}/0",
        "etype {etype} ;etime {etime}",
    ],
    ("element", "solid"): [
        "genselect clear all",
        "genselect solid add solid {element_id}/0",
        "etype {etype} ;etime {etime}",
    ],
    ("node", None): [
        "genselect clear all",
        "genselect node add node {element_id}",
    ],
}


def build_command(name: str, props: Dict[str, Any]) -> str:
    """Сформировать команду обработки одной кривой."""
    safe = safe_name(name)
    parts = [f"--{k}={v}" for k, v in sorted(props.items())]
    return " ".join([safe] + parts)


def build_curve_commands(
    base_project_dir: str,
    top_folder_name: str,
    analysis_type: str,
    entity_kind: str,
    element_type: str | None,
    element_id: int,
    curves_dirname: str = "curves",
    analysis_dirname: str | None = None,
) -> List[str]:
    """Построить последовательность команд для сохранения кривой.

    Возвращает список строк без символов перевода строки.
    """

    if not analysis_type:
        raise ValueError("analysis_type must be non-empty")
    if element_id <= 0:
        raise ValueError("element_id must be positive")
    if entity_kind not in {"element", "node"}:
        raise ValueError("unknown entity_kind")
    if entity_kind == "element":
        if element_type not in {"beam", "shell", "solid"}:
            raise ValueError("invalid element_type for element")
    else:
        if element_type is not None:
            raise ValueError("element_type must be None for node")

    key = (entity_kind, element_type)
    try:
        template = SELECT_TEMPLATES[key]
    except KeyError as exc:  # pragma: no cover - should not happen after validation
        raise ValueError("unsupported entity selection") from exc

    etype = None
    if element_type is not None:
        try:
            etype = ETYPE_BY_ELEMENT[element_type]
        except KeyError as exc:  # pragma: no cover - validated above
            raise ValueError("unsupported element_type") from exc

    try:
        if element_type is None:
            etime = ANALYSIS_TYPE_CODES["beam"][analysis_type]
        else:
            etime = ANALYSIS_TYPE_CODES[element_type][analysis_type]
    except KeyError as exc:
        raise ValueError("unsupported analysis_type") from exc

    select_cmds = [
        cmd.format(element_id=element_id, etype=etype, etime=etime) for cmd in template
    ]

    curve_path = PureWindowsPath(
        base_project_dir,
        curves_dirname,
        top_folder_name,
        analysis_dirname or analysis_type,
        f"{element_id}.txt",
    )

    save_cmds = [
        f'xyplot 1 savefile curve_file "{curve_path}" 1 all',
        "xyplot 1 donemenu",
        "deletewin 1",
    ]

    return select_cmds + save_cmds


__all__ = ["build_command", "build_curve_commands"]
