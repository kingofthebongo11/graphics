"""Сканирование файлов кривых."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List


def scan_curves(root_dir: Path | str) -> Dict[str, Dict[str, List[str]]]:
    """Сканирует каталог с кривыми и собирает файлы по топ-папкам.

    Параметры:
        root_dir: Корневая директория, содержащая топ-папки.

    Возвращает:
        Словарь вида ``{топ_папка: {тип_анализа: [пути к файлам]}}``.
    """
    root_path = Path(root_dir)
    result: Dict[str, Dict[str, List[str]]] = {}

    if not root_path.exists():
        return result

    for top_path in root_path.iterdir():
        if not top_path.is_dir():
            continue

        analyses: Dict[str, List[str]] = {}
        for analysis_dir in top_path.iterdir():
            if not analysis_dir.is_dir():
                continue

            files: List[str] = []
            for file_path in analysis_dir.iterdir():
                if file_path.is_file() and file_path.suffix in {".png", ".txt"}:
                    files.append(str(file_path))

            if files:
                analyses[analysis_dir.name] = files

        if analyses:
            result[top_path.name] = analyses

    return result
