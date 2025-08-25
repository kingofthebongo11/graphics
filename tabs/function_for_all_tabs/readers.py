from __future__ import annotations

from pathlib import Path
from typing import Callable, List, Tuple

from tabs.functions_for_tab1.curves_from_file import (
    read_X_Y_from_excel,
    read_X_Y_from_ls_dyna,
    read_X_Y_from_text_file,
)


def read_pairs_any(
    path: str,
    *,
    read_excel: Callable[[dict], None] = read_X_Y_from_excel,
    read_ls_dyna: Callable[[dict], None] = read_X_Y_from_ls_dyna,
    read_text: Callable[[dict], None] = read_X_Y_from_text_file,
) -> Tuple[List[float], List[float]]:
    """Read ``(X, Y)`` pairs from a file of any supported format.

    Parameters
    ----------
    path:
        Путь к файлу данных.
    read_excel, read_ls_dyna, read_text:
        Функции чтения для форматов Excel, LS-DYNA и текстовых файлов.
        Передаются как параметры для упрощения тестирования.
    """
    path = Path(path).resolve()
    curve_info = {"curve_file": path}
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xlsm", ".csv"}:
        read_excel(curve_info)
    else:
        try:
            read_ls_dyna(curve_info)
        except Exception:
            read_text(curve_info)
        else:
            if "X_values" not in curve_info or "Y_values" not in curve_info:
                read_text(curve_info)
    return curve_info.get("X_values", []), curve_info.get("Y_values", [])


__all__ = ["read_pairs_any"]
