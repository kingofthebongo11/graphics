"""Рабочий процесс генерации графиков и отчёта."""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple
import logging

from curves_scan import scan_curves
from plot_from_txt import plot_from_txt_files

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
        structure, scan_errors = scan_curves(root)
        if scan_errors:
            (root / "errors.log").write_text("\n".join(scan_errors), encoding="utf-8")
            logging.warning(
                "Обнаружены проблемы при сканировании, см. errors.log"
            )
        errors.extend(scan_errors)
    except Exception as exc:  # pragma: no cover - защитный код
        errors.append(f"Сканирование: {exc}")
        structure = {}

    for analyses in structure.values():
        for analysis_type, files in analyses.items():
            analysis_dir = Path(files[0]).parent
            txt_files = [f for f in files if f.lower().endswith(".txt")]
            png_file = analysis_dir.with_suffix(".png")
            if txt_files and not png_file.exists():
                try:
                    plot_from_txt_files(txt_files, analysis_type)
                except Exception as exc:  # pragma: no cover - отсутствие GUI
                    errors.append(f"{analysis_dir}: {exc}")

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
