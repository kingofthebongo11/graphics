from __future__ import annotations

"""Построение PNG-графика по данным из текстового файла.

Стили оформления и обработка подписей осей переиспользуются из утилит
Tab1, используемых в графическом интерфейсе проекта.
"""

from pathlib import Path
import argparse

from tabs.function_for_all_tabs.validation import ensure_analysis_type
from tabs.functions_for_tab1.curves_from_file.text_file import (
    read_X_Y_from_text_file,
)
from tabs.function_for_all_tabs import create_plot
from tabs.title_utils import format_signature


def extract_labels(analysis_type: str) -> tuple[str, str]:
    """Получить подписи осей из ``analysis_type``.

    Parameters
    ----------
    analysis_type:
        Строка вида ``"Время-Продольная сила"``.

    Returns
    -------
    tuple[str, str]
        Подписи осей ``(X, Y)`` с применённым форматированием.
    """

    atype = ensure_analysis_type(analysis_type)
    x_raw, y_raw = (part.strip() for part in atype.split("-", 1))
    return (
        format_signature(x_raw, bold=False),
        format_signature(y_raw, bold=False),
    )


def plot_from_txt(txt_file: str, analysis_type: str, output: str | None = None) -> str:
    """Построить график и сохранить его в PNG.

    Parameters
    ----------
    txt_file:
        Путь к текстовому файлу с двумя столбцами чисел ``X Y``.
    analysis_type:
        Тип анализа из :mod:`analysis_types`.
    output:
        Путь для сохранения PNG. Если не указан, используется имя входного
        файла с расширением ``.png``.

    Returns
    -------
    str
        Путь к сохранённому файлу PNG.
    """

    curve_info: dict[str, list[float]] = {"curve_file": txt_file}
    read_X_Y_from_text_file(curve_info)
    if "X_values" not in curve_info or "Y_values" not in curve_info:
        raise ValueError("Не удалось прочитать данные из текстового файла")

    x_label, y_label = extract_labels(analysis_type)
    output_path = output or str(Path(txt_file).with_suffix(".png"))

    create_plot(
        [curve_info],
        x_label=x_label,
        y_label=y_label,
        title="",
        save_file=True,
        file_plt=output_path,
    )
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Построить PNG-график по данным из текстового файла",
    )
    parser.add_argument("txt_file", help="Путь к входному TXT файлу")
    parser.add_argument(
        "analysis_type",
        help="Тип анализа, например 'Время-Продольная сила'",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Путь для сохранения PNG",
        default=None,
    )
    args = parser.parse_args()
    plot_from_txt(args.txt_file, args.analysis_type, args.output)


if __name__ == "__main__":
    main()
