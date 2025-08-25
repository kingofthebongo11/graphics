"""Сканирование файлов кривых."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple


def scan_curves(root_dir: Path | str) -> Tuple[Dict[str, Dict[str, List[str]]], List[str]]:
    """Сканирует каталог с кривыми и собирает файлы по топ-папкам.

    Параметры:
        root_dir: Корневая директория, содержащая топ-папки.

    Возвращает:
        Кортеж ``(структура, ошибки)``. ``структура`` имеет вид
        ``{топ_папка: {тип_анализа: [пути к файлам]}}``.
    """
    root_path = Path(root_dir)
    result: Dict[str, Dict[str, List[str]]] = {}
    errors: List[str] = []

    if not root_path.exists():
        errors.append(f"Корневая директория '{root_path}' не найдена")
        return result, errors

    top_dirs = [p for p in root_path.iterdir() if p.is_dir()]
    if not top_dirs:
        errors.append("Не найдено ни одной топ-папки")
        return result, errors

    for top_path in top_dirs:
        analyses: Dict[str, List[str]] = {}
        had_subdirs = False
        for analysis_dir in top_path.iterdir():
            if not analysis_dir.is_dir():
                continue

            had_subdirs = True
            files: List[str] = []
            for file_path in analysis_dir.iterdir():
                if file_path.is_file() and file_path.suffix in {".png", ".txt"}:
                    files.append(str(file_path))

            if files:
                analyses[analysis_dir.name] = files
            else:
                errors.append(
                    f"Подпапка анализа '{analysis_dir.name}' в топ-папке "
                    f"'{top_path.name}' не содержит файлов"
                )

        if analyses:
            result[top_path.name] = analyses
        elif not had_subdirs:
            errors.append(
                f"Топ-папка '{top_path.name}' не содержит подпапок анализов"
            )

    return result, errors
