from __future__ import annotations

"""Построение PNG-графика по данным из файла.

Стили оформления и обработка подписей осей переиспользуются из утилит
Tab1, используемых в графическом интерфейсе проекта. Файл может быть
как простым текстовым, так и в формате LS-DYNA.
"""

from pathlib import Path
import argparse

from tabs.function_for_all_tabs.validation import ensure_analysis_type
from tabs.function_for_all_tabs import create_plot, read_pairs_any
from tabs.functions_for_tab1.plotting import TitleProcessor
from tabs.constants import (
    DEFAULT_UNITS,
    TITLE_TRANSLATIONS,
    TITLES_SYMBOLS,
    LEGEND_TITLE_TRANSLATIONS,
)
from topfolder_codec import decode_topfolder


def extract_labels(analysis_type: str) -> tuple[str, str, str]:
    """Получить подписи осей и заголовок из ``analysis_type``.

    Parameters
    ----------
    analysis_type:
        Строка вида ``"Время - Продольная сила"``.

    Returns
    -------
    tuple[str, str, str]
        Подписи осей ``(X, Y)`` и заголовок ``title`` с оформленными
        обозначениями и единицами измерения.
    """

    atype = ensure_analysis_type(analysis_type)
    x_raw, y_raw = (part.strip() for part in atype.split("-", 1))

    class Getter:
        def __init__(self, value: str):
            self._value = value

        def get(self) -> str:
            return self._value

    x_title = Getter(x_raw)
    y_title = Getter(y_raw)
    x_unit = Getter(DEFAULT_UNITS.get(x_raw, ""))
    y_unit = Getter(DEFAULT_UNITS.get(y_raw, ""))

    x_proc = TitleProcessor(
        x_title, combo_size=x_unit, translations=TITLE_TRANSLATIONS
    )
    y_proc = TitleProcessor(
        y_title, combo_size=y_unit, translations=TITLE_TRANSLATIONS
    )
    title_proc = TitleProcessor(
        y_title, combo_size=y_unit, translations=TITLES_SYMBOLS, bold_math=True
    )

    xlabel = x_proc.get_processed_title()
    ylabel = y_proc.get_processed_title()
    title = title_proc.get_processed_title()
    return xlabel, ylabel, title


def plot_from_txt(txt_file: str, analysis_type: str, output: str | None = None) -> str:
    """Построить график и сохранить его в PNG.

    Parameters
    ----------
    txt_file:
        Путь к файлу с числовыми данными ``X Y``. Поддерживаются текстовый
        формат и файлы LS-DYNA.
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

    xs, ys = read_pairs_any(txt_file)
    if not xs or not ys:
        raise ValueError("Не удалось прочитать данные из файла")

    curve_info = {"curve_file": txt_file, "X_values": xs, "Y_values": ys}

    x_label, y_label, title = extract_labels(analysis_type)
    output_path = output or str(Path(txt_file).with_suffix(".png"))

    create_plot(
        [curve_info],
        x_label=x_label,
        y_label=y_label,
        title=title,
        save_file=True,
        file_plt=output_path,
    )
    return output_path


def plot_from_txt_files(txt_files: list[str], analysis_type: str) -> str:
    """Построить график по нескольким файлам и сохранить его рядом с папкой анализа.

    Parameters
    ----------
    txt_files:
        Список путей к файлам с данными ``X Y``.
    analysis_type:
        Тип анализа из :mod:`analysis_types`.

    Returns
    -------
    str
        Путь к сохранённому файлу PNG.
    """

    if not txt_files:
        raise ValueError("Не передано ни одного файла")

    curves: list[dict[str, object]] = []
    for file in txt_files:
        xs, ys = read_pairs_any(file)
        if not xs or not ys:
            continue
        curves.append(
            {
                "curve_file": file,
                "X_values": xs,
                "Y_values": ys,
                "curve_legend": Path(file).stem,
            }
        )

    if not curves:
        raise ValueError("Не удалось прочитать данные из файлов")

    x_label, y_label, title = extract_labels(analysis_type)
    analysis_dir = Path(txt_files[0]).parent
    output_path = str(analysis_dir.with_suffix(".png"))

    _, entity_kind, _ = decode_topfolder(analysis_dir.parent.name)
    legend_key = "№ Элементов" if entity_kind == "element" else "№ Узлов"
    legend_title = LEGEND_TITLE_TRANSLATIONS[legend_key]["Русский"]

    create_plot(
        curves,
        x_label=x_label,
        y_label=y_label,
        title=title,
        legend=True,
        legend_title=legend_title,
        save_file=True,
        file_plt=output_path,
    )
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Построить PNG-график по данным из файла",
    )
    parser.add_argument("txt_file", help="Путь к входному файлу с данными")
    parser.add_argument(
        "analysis_type",
        help="Тип анализа, например 'Время - Продольная сила'",
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
