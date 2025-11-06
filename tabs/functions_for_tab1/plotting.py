from tkinter import filedialog, messagebox
from pathlib import Path
import logging

from tabs.function_for_all_tabs import create_plot
from .curves_from_file import (
    read_X_Y_from_frequency_analysis,
    read_X_Y_from_text_file,
    read_X_Y_from_ls_dyna,
    read_X_Y_from_excel,
    read_X_Y_from_combined,
)
from tabs.constants import (
    TITLES_SYMBOLS,
    TITLE_TRANSLATIONS,
    PHYSICAL_QUANTITIES_EN_TO_RU,
    PHYSICAL_QUANTITIES_TRANSLATION,
    UNITS_TRANSLATION,
    LEGEND_TITLE_TRANSLATIONS,
)
from tabs.title_utils import format_signature

logger = logging.getLogger(__name__)

# Хранит информацию о последнем построенном графике для последующего сохранения
last_graph = {}


def _parse_manual_axis_value(entry, axis_label: str, bound_label: str):
    """Преобразовать текст из поля ручного ввода оси в число."""

    if entry is None or not hasattr(entry, "get"):
        return None
    if not getattr(entry, "user_modified", False):
        return None
    text = entry.get().strip()
    if not text:
        setattr(entry, "user_modified", False)
        return None
    normalized = text.replace(",", ".")
    try:
        return float(normalized)
    except ValueError as exc:  # pragma: no cover - защита от пользовательского ввода
        raise ValueError(
            f"Некорректное значение для оси {axis_label} ({bound_label}): {text}"
        ) from exc


def apply_axis_limits(ax, canvas, axis_manual_entries=None):
    """Применить ручные пределы осей к уже построенному графику."""

    if axis_manual_entries is None:
        return False
    if not hasattr(ax, "has_data") or not ax.has_data():
        messagebox.showwarning("Предупреждение", "Сначала постройте график")
        return False
    try:
        x_min_manual = _parse_manual_axis_value(
            axis_manual_entries.get("x_min"), "X", "от"
        )
        x_max_manual = _parse_manual_axis_value(
            axis_manual_entries.get("x_max"), "X", "до"
        )
        y_min_manual = _parse_manual_axis_value(
            axis_manual_entries.get("y_min"), "Y", "от"
        )
        y_max_manual = _parse_manual_axis_value(
            axis_manual_entries.get("y_max"), "Y", "до"
        )
    except ValueError as exc:
        messagebox.showerror("Ошибка", str(exc))
        return False

    if (
        x_min_manual is not None
        and x_max_manual is not None
        and x_min_manual >= x_max_manual
    ):
        messagebox.showerror(
            "Ошибка", "Значение «от» должно быть меньше значения «до» для оси X."
        )
        return False
    if (
        y_min_manual is not None
        and y_max_manual is not None
        and y_min_manual >= y_max_manual
    ):
        messagebox.showerror(
            "Ошибка", "Значение «от» должно быть меньше значения «до» для оси Y."
        )
        return False

    limits_changed = False
    if x_min_manual is not None or x_max_manual is not None:
        current_xlim = ax.get_xlim()
        ax.set_xlim(
            x_min_manual if x_min_manual is not None else current_xlim[0],
            x_max_manual if x_max_manual is not None else current_xlim[1],
        )
        limits_changed = True
    if y_min_manual is not None or y_max_manual is not None:
        current_ylim = ax.get_ylim()
        ax.set_ylim(
            y_min_manual if y_min_manual is not None else current_ylim[0],
            y_max_manual if y_max_manual is not None else current_ylim[1],
        )
        limits_changed = True

    if limits_changed:
        if hasattr(canvas, "draw_idle"):
            canvas.draw_idle()
        else:
            canvas.draw()
    return limits_changed


class TitleProcessor:
    def __init__(
        self,
        combo_title,
        combo_size=None,
        entry_title=None,
        language="Русский",
        bold_math: bool = False,
        translations=None,
    ):
        self.combo_title = combo_title
        self.combo_size = combo_size
        self.entry_title = entry_title
        self.language = language
        self.bold_math = bold_math
        if translations is None:
            translations = TITLES_SYMBOLS
        self.translations = translations

    def _get_ru_en_quantity(self):
        selection = self.combo_title.get()
        if selection in PHYSICAL_QUANTITIES_TRANSLATION:
            ru = selection
            en = PHYSICAL_QUANTITIES_TRANSLATION[selection]
        else:
            en = selection
            ru = PHYSICAL_QUANTITIES_EN_TO_RU.get(selection, selection)
        return ru, en

    def _get_units(self):
        if self.combo_size is None:
            return ""
        unit_ru = self.combo_size.get()
        if unit_ru in ("", "Нет"):
            return ""
        ru, _ = self._get_ru_en_quantity()
        unit = unit_ru
        if self.language == "Английский":
            units_dict = UNITS_TRANSLATION.get(ru)
            if units_dict:
                unit = units_dict.get(unit_ru, unit_ru)
        if unit in ("", "None"):
            return ""
        return f", {unit}"

    def _get_title(self):
        ru, _ = self._get_ru_en_quantity()
        return self.translations.get(ru, {}).get(
            self.language, self.combo_title.get()
        )

    def get_processed_title(self) -> str:
        """Вернуть заголовок с оформленными обозначениями."""
        selection = self.combo_title.get()
        if selection in ("Другое", ""):
            result = self.entry_title.get() if self.entry_title else ""
        elif selection == "Нет":
            result = ""
        else:
            title = self._get_title()
            result = f"{title}{self._get_units()}"
        return format_signature(result, bold=self.bold_math)

def save_file(entry_widget, format_widget, graph_info):

    fig = graph_info.get("fig")
    if fig is None:
        messagebox.showwarning("Предупреждение", "Сначала постройте график")
        return

    file_name = entry_widget.get()
    file_format = format_widget.get()
    if file_name and file_format:
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{file_format}",
            filetypes=[
                (f"{file_format.upper()} files", f"*.{file_format}"),
                ("All files", "*.*"),
            ],
            initialfile=f"{file_name}.{file_format}",
        )
        if file_path:
            try:
                fig.savefig(file_path, format=file_format)
                messagebox.showinfo("Успех", f"График сохранен: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    elif not file_name:
        messagebox.showerror("Ошибка", "Имя файла не может быть пустым!")
    else:
        messagebox.showerror("Ошибка", "Не выбран формат файла!")


def get_X_Y_data(curve_info):
    curve_type = curve_info.get("curve_type")
    if curve_type == "Текстовой файл":
        read_X_Y_from_text_file(curve_info)
    elif curve_type == "Файл кривой LS-Dyna":
        read_X_Y_from_ls_dyna(curve_info)
    elif curve_type == "Excel файл":
        read_X_Y_from_excel(curve_info)
    elif curve_type == "Частотный анализ":
        read_X_Y_from_frequency_analysis(curve_info)
    elif curve_type == "Комбинированный":
        read_X_Y_from_combined(curve_info)


def generate_graph(
    ax,
    fig,
    canvas,
    combo_title,
    entry_title_custom,
    combo_titleX,
    combo_titleX_size,
    entry_titleX,
    combo_titleY,
    combo_titleY_size,
    entry_titleY,
    legend_checkbox,
    curves_frame,
    combo_curves,
    combo_language,
    legend_title_combo,
    legend_title_entry,
    legend_title_var,
    axis_auto_entries=None,
    axis_manual_entries=None,
):

    # Очистка предыдущего графика
    ax.clear()
    language = combo_language.get() or "Русский"
    title_processor = TitleProcessor(
        combo_title,
        entry_title=entry_title_custom,
        language=language,
        bold_math=True,
    )
    xlabel_processor = TitleProcessor(
        combo_titleX,
        combo_titleX_size,
        entry_titleX,
        language,
        bold_math=False,
        translations=TITLE_TRANSLATIONS,
    )
    ylabel_processor = TitleProcessor(
        combo_titleY,
        combo_titleY_size,
        entry_titleY,
        language,
        bold_math=False,
        translations=TITLE_TRANSLATIONS,
    )
    title = title_processor.get_processed_title()
    xlabel = xlabel_processor.get_processed_title()
    ylabel = ylabel_processor.get_processed_title()

    def _set_entry_value(entry, value: str) -> None:
        if entry is None or not hasattr(entry, "delete"):
            return
        state = entry.cget("state") if hasattr(entry, "cget") else None
        if state is not None:
            entry.config(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        if state is not None:
            entry.config(state=state)

    def _update_auto_limits(values, min_entry, max_entry) -> None:
        if values:
            _set_entry_value(min_entry, f"{min(values):.6g}")
            _set_entry_value(max_entry, f"{max(values):.6g}")
        else:
            _set_entry_value(min_entry, "-")
            _set_entry_value(max_entry, "-")

    def _sync_manual_with_auto(auto_entries, manual_entries) -> None:
        if not auto_entries or not manual_entries:
            return
        for key in ("x_min", "x_max", "y_min", "y_max"):
            manual_entry = manual_entries.get(key) if manual_entries else None
            if manual_entry is None or not hasattr(manual_entry, "get"):
                continue
            if manual_entry.get().strip() == "":
                setattr(manual_entry, "user_modified", False)
            if getattr(manual_entry, "user_modified", False):
                continue
            auto_entry = auto_entries.get(key) if auto_entries else None
            if auto_entry is None or not hasattr(auto_entry, "get"):
                continue
            value = auto_entry.get().strip()
            if value == "-":
                _set_entry_value(manual_entry, "")
                setattr(manual_entry, "user_modified", False)
                continue
            if value:
                _set_entry_value(manual_entry, value)
                setattr(manual_entry, "user_modified", False)

    # Текст заголовка передается без LaTeX-команд,
    # оформление выполняется через параметры Matplotlib.

    if combo_titleX.get() == "Другое" and (
        entry_titleX is None or not entry_titleX.get().strip()
    ):
        messagebox.showwarning("Предупреждение", "Заполните название оси X")
        return

    if combo_titleY.get() == "Другое" and (
        entry_titleY is None or not entry_titleY.get().strip()
    ):
        messagebox.showwarning("Предупреждение", "Заполните название оси Y")
        return

    if legend_checkbox.get():
        other_label = LEGEND_TITLE_TRANSLATIONS["Другое"].get(language, "Другое")
        none_label = LEGEND_TITLE_TRANSLATIONS["Нет"].get(language, "Нет")
        selected = legend_title_var.get() if legend_title_var else ""
        entry_visible = (
            legend_title_entry.winfo_ismapped()
            if legend_title_entry and hasattr(legend_title_entry, "winfo_ismapped")
            else False
        )
        if entry_visible or selected == other_label:
            text = legend_title_entry.get().strip() if legend_title_entry else ""
            if not text:
                messagebox.showwarning("Предупреждение", "Заполните подпись легенды")
                return
            legend_title = text
        elif selected == none_label or not selected:
            legend_title = None
        else:
            legend_title = selected
        if legend_title:
            legend_title = format_signature(legend_title, bold=False)
    else:
        legend_title = None

    # Считываем количество кривых из combobox
    num_curves = int(combo_curves.get())

    curves_info = []
    # Построение каждой кривой в цикле
    for i in range(1, num_curves + 1):
        curve_info = {}
        for widget in curves_frame.winfo_children():
            if hasattr(widget, "_name"):
                widget_name = widget._name

                # Проверяем тип кривой
                if widget_name == f"curve_{i}_type":
                    curve_info["curve_type"] = widget.get()

                # Если тип кривой "Частотный анализ", собираем дополнительные данные
                if (
                    "curve_type" in curve_info
                    and curve_info["curve_type"] == "Частотный анализ"
                ):
                    if widget_name == f"curve_{i}_typeXF":
                        curve_info["curve_typeXF"] = widget.get()
                    elif widget_name == f"curve_{i}_typeYF":
                        curve_info["curve_typeYF"] = widget.get()
                    elif widget_name == f"curve_{i}_typeXFtype":
                        curve_info["curve_typeXF_type"] = widget.get()
                    elif widget_name == f"curve_{i}_typeYFtype":
                        curve_info["curve_typeYF_type"] = widget.get()

                if widget_name == f"curve_{i}_X_source":
                    curve_info.setdefault("X_source", {}).update(
                        {"source": widget.get()}
                    )
                elif widget_name == f"curve_{i}_Y_source":
                    curve_info.setdefault("Y_source", {}).update(
                        {"source": widget.get()}
                    )
                elif widget_name == f"curve_{i}_X_parameter":
                    curve_info.setdefault("X_source", {}).update(
                        {"parameter": widget.get()}
                    )
                elif widget_name == f"curve_{i}_Y_parameter":
                    curve_info.setdefault("Y_source", {}).update(
                        {"parameter": widget.get()}
                    )
                elif widget_name == f"curve_{i}_X_direction":
                    curve_info.setdefault("X_source", {}).update(
                        {"direction": widget.get()}
                    )
                elif widget_name == f"curve_{i}_Y_direction":
                    curve_info.setdefault("Y_source", {}).update(
                        {"direction": widget.get()}
                    )
                elif widget_name == f"curve_{i}_X_column":
                    value = widget.get()
                    column = 0 if value != "Y" else 1
                    curve_info.setdefault("X_source", {}).update({"column": column})
                elif widget_name == f"curve_{i}_Y_column":
                    value = widget.get()
                    column = 1 if value != "X" else 0
                    curve_info.setdefault("Y_source", {}).update({"column": column})
                elif widget_name == f"curve_{i}_X_range":
                    curve_info.setdefault("X_source", {}).update(
                        {"range_x": widget.get(), "use_ranges": True}
                    )
                elif widget_name == f"curve_{i}_Y_range":
                    curve_info.setdefault("Y_source", {}).update(
                        {"range_y": widget.get(), "use_ranges": True}
                    )

                # Получаем имя файла для каждой кривой
                if widget_name == f"curve_{i}_filename":
                    curve_info["curve_file"] = widget.get()
                    if curve_info.get("curve_type") != "Комбинированный":
                        if "X_source" in curve_info:
                            curve_info["X_source"].setdefault(
                                "curve_file", widget.get()
                            )
                        if "Y_source" in curve_info:
                            curve_info["Y_source"].setdefault(
                                "curve_file", widget.get()
                            )
                elif widget_name == f"curve_{i}_filename_X":
                    curve_info.setdefault("X_source", {}).update(
                        {"curve_file": widget.get()}
                    )
                elif widget_name == f"curve_{i}_filename_Y":
                    curve_info.setdefault("Y_source", {}).update(
                        {"curve_file": widget.get()}
                    )
                if widget_name == f"curve_{i}_horizontal":
                    curve_info["horizontal"] = widget.var.get()

                if widget_name == f"curve_{i}_use_offset":
                    curve_info["use_offset"] = widget.var.get()
                elif widget_name == f"curve_{i}_offset_h":
                    try:
                        curve_info["offset_horizontal"] = int(widget.get())
                    except ValueError:
                        curve_info["offset_horizontal"] = 0
                elif widget_name == f"curve_{i}_offset_v":
                    try:
                        curve_info["offset_vertical"] = int(widget.get())
                    except ValueError:
                        curve_info["offset_vertical"] = 0
                if widget_name == f"curve_{i}_use_ranges":
                    curve_info["use_ranges"] = widget.var.get()
                elif widget_name == f"curve_{i}_range_x":
                    curve_info["range_x"] = widget.get()
                elif widget_name == f"curve_{i}_range_y":
                    curve_info["range_y"] = widget.get()
                elif widget_name == f"curve_{i}_slider_start":
                    try:
                        curve_info["slider_start"] = float(widget.get())
                    except (TypeError, ValueError):
                        curve_info["slider_start"] = 0.0
                elif widget_name == f"curve_{i}_slider_end":
                    try:
                        curve_info["slider_end"] = float(widget.get())
                    except (TypeError, ValueError):
                        curve_info["slider_end"] = 100.0

                # Проверяем наличие легенды, если отмечен чекбокс
                if legend_checkbox.get() and widget_name == f"curve_{i}_legend":
                    curve_info["curve_legend"] = widget.get()
        if legend_checkbox.get() and not curve_info.get("curve_legend", "").strip():
            messagebox.showwarning(
                "Предупреждение", f"Введите подпись легенды для кривой {i}"
            )
            return
        # Проверяем источники и файлы данных для кривой
        if curve_info.get("curve_type") == "Комбинированный":
            for axis in ["X", "Y"]:
                source_info = curve_info.get(f"{axis}_source", {})
                if not source_info.get("source"):
                    messagebox.showerror(
                        "Ошибка", f"Не указан источник {axis} для кривой {i}"
                    )
                    return
                file = source_info.get("curve_file")
                if not file:
                    messagebox.showerror(
                        "Ошибка", f"Не указан файл данных для кривой {i}"
                    )
                    return
                if not Path(file).exists():
                    messagebox.showerror("Ошибка", f"Файл {file} не найден")
                    return
        else:
            file = curve_info.get("curve_file")
            if not file:
                messagebox.showerror("Ошибка", f"Не указан файл данных для кривой {i}")
                return
            if not Path(file).exists():
                messagebox.showerror("Ошибка", f"Файл {file} не найден")
                return
        # Добавляем информацию о кривой в общий список
        if "X_source" in curve_info and "column" not in curve_info["X_source"]:
            curve_info["X_source"]["column"] = 0
        if "Y_source" in curve_info and "column" not in curve_info["Y_source"]:
            curve_info["Y_source"]["column"] = 1
        get_X_Y_data(curve_info)
        slider_start = max(0.0, min(100.0, float(curve_info.get("slider_start", 0.0))))
        slider_end = max(0.0, min(100.0, float(curve_info.get("slider_end", 100.0))))
        x_values = curve_info.get("X_values", [])
        y_values = curve_info.get("Y_values", [])
        if not x_values or not y_values:
            messagebox.showerror(
                "Ошибка", f"Не удалось получить данные для кривой {i}"
            )
            return
        if len(x_values) != len(y_values):
            messagebox.showerror(
                "Ошибка",
                f"Количество точек X и Y для кривой {i} не совпадает",
            )
            return
        if len(x_values) > 1:
            start_idx = int(round((len(x_values) - 1) * slider_start / 100))
            end_idx = int(round((len(x_values) - 1) * slider_end / 100))
        else:
            start_idx = end_idx = 0
        if end_idx < start_idx:
            start_idx, end_idx = end_idx, start_idx
        start_idx = max(0, min(start_idx, len(x_values) - 1))
        end_idx = max(start_idx, min(end_idx, len(x_values) - 1))
        slice_obj = slice(start_idx, end_idx + 1)
        curve_info["X_values"] = x_values[slice_obj]
        curve_info["Y_values"] = y_values[slice_obj]
        if not curve_info["X_values"] or not curve_info["Y_values"]:
            messagebox.showerror(
                "Ошибка",
                f"После применения фильтра точек для кривой {i} не осталось данных",
            )
            return
        curves_info.append(curve_info)

    if axis_auto_entries:
        x_values_all = [
            value for curve in curves_info for value in curve.get("X_values", [])
        ]
        y_values_all = [
            value for curve in curves_info for value in curve.get("Y_values", [])
        ]
        _update_auto_limits(
            x_values_all,
            axis_auto_entries.get("x_min"),
            axis_auto_entries.get("x_max"),
        )
        _update_auto_limits(
            y_values_all,
            axis_auto_entries.get("y_min"),
            axis_auto_entries.get("y_max"),
        )
        _sync_manual_with_auto(axis_auto_entries, axis_manual_entries)

    x_min_manual = x_max_manual = y_min_manual = y_max_manual = None
    if axis_manual_entries:
        try:
            x_min_manual = _parse_manual_axis_value(
                axis_manual_entries.get("x_min"), "X", "от"
            )
            x_max_manual = _parse_manual_axis_value(
                axis_manual_entries.get("x_max"), "X", "до"
            )
            y_min_manual = _parse_manual_axis_value(
                axis_manual_entries.get("y_min"), "Y", "от"
            )
            y_max_manual = _parse_manual_axis_value(
                axis_manual_entries.get("y_max"), "Y", "до"
            )
        except ValueError as exc:
            messagebox.showerror("Ошибка", str(exc))
            return
        if (
            x_min_manual is not None
            and x_max_manual is not None
            and x_min_manual >= x_max_manual
        ):
            messagebox.showerror(
                "Ошибка", "Значение «от» должно быть меньше значения «до» для оси X."
            )
            return
        if (
            y_min_manual is not None
            and y_max_manual is not None
            and y_min_manual >= y_max_manual
        ):
            messagebox.showerror(
                "Ошибка", "Значение «от» должно быть меньше значения «до» для оси Y."
            )
            return

    logger.debug("Передача подписей осей в create_plot: X=%r, Y=%r", xlabel, ylabel)
    try:
        create_plot(
            curves_info,
            xlabel,
            ylabel,
            title,
            fig=fig,
            ax=ax,
            legend=legend_checkbox.get(),
            legend_title=legend_title,
            title_fontstyle="normal",
        )
        if axis_manual_entries:
            if x_min_manual is not None or x_max_manual is not None:
                current_xlim = ax.get_xlim()
                ax.set_xlim(
                    x_min_manual
                    if x_min_manual is not None
                    else current_xlim[0],
                    x_max_manual
                    if x_max_manual is not None
                    else current_xlim[1],
                )
            if y_min_manual is not None or y_max_manual is not None:
                current_ylim = ax.get_ylim()
                ax.set_ylim(
                    y_min_manual
                    if y_min_manual is not None
                    else current_ylim[0],
                    y_max_manual
                    if y_max_manual is not None
                    else current_ylim[1],
                )
    except ValueError as exc:
        if exc.__cause__ is not None and isinstance(exc.__cause__, ValueError):
            logger.error("Ошибка разметки подписи", exc_info=True)
            raise ValueError(
                f"{exc}\nСбой связан с неправильной разметкой подписи."
            ) from exc
        logger.error("Ошибка при построении графика", exc_info=True)
        raise

    # Сохраняем данные графика для последующего сохранения в файл
    global last_graph
    last_graph.clear()
    last_graph.update(
        {
            "curves_info": curves_info,
            "x_label": xlabel,
            "y_label": ylabel,
            "title": title,
            "fig": fig,
        }
    )

    # Перерисовка графика
    canvas.draw()
