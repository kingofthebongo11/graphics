"""Рабочий процесс генерации графиков и отчёта."""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from curves_scan import scan_curves
from plot_from_txt import plot_from_txt

try:  # pragma: no cover - зависимость может отсутствовать
    from report_docx import build_report
except Exception:  # noqa: BLE001 - перехват любых ошибок импорта
    build_report = None  # type: ignore[assignment]


def build_curves_report(curves_root: Path | str) -> Tuple[Path | None, List[str]]:
    """Сканирует каталоги, строит PNG и формирует DOCX.

    Параметры:
        curves_root: Корневая папка, содержащая топ-папки с анализами.

    Возвращает:
        Кортеж ``(путь к Report.docx или None, список ошибок)``.
    """
    root = Path(curves_root)
    errors: List[str] = []

    try:
        structure = scan_curves(root)
    except Exception as exc:  # pragma: no cover - защитный код
        errors.append(f"Сканирование: {exc}")
        structure = {}

    for analyses in structure.values():
        for analysis_type, files in analyses.items():
            existing_pngs = {Path(f) for f in files if f.lower().endswith(".png")}
            for txt_file in (Path(f) for f in files if f.lower().endswith(".txt")):
                png_file = txt_file.with_suffix(".png")
                if png_file not in existing_pngs:
                    try:
                        plot_from_txt(str(txt_file), analysis_type, str(png_file))
                        existing_pngs.add(png_file)
                    except Exception as exc:  # pragma: no cover - отсутствие GUI
                        errors.append(f"{txt_file}: {exc}")

    docx_path: Path | None = None
    if build_report is None:
        errors.append("DOCX: модуль python-docx недоступен")
    else:
        try:
            docx_path = build_report(root)
        except Exception as exc:  # pragma: no cover - защитный код
            errors.append(f"DOCX: {exc}")

    return docx_path, errors


__all__ = ["build_curves_report"]
