from tkinter import filedialog, messagebox
from pathlib import Path

from tabs.function_for_all_tabs import create_plot
from .curves_from_file import (
    read_X_Y_from_frequency_analysis,
    read_X_Y_from_text_file,
    read_X_Y_from_ls_dyna,
    read_X_Y_from_excel,
    read_X_Y_from_combined,
)

# Хранит информацию о последнем построенном графике для последующего сохранения
last_graph = {}

title_mapping = {
    "Время": {
        "Русский": "Время $t$",
        "Английский": "Time $t$",
    },
    "Перемещение по X": {
        "Русский": "Перемещение $x$",
        "Английский": "Displacement $x$",
    },
    "Перемещение по Y": {
        "Русский": "Перемещение $y$",
        "Английский": "Displacement $y$",
    },
    "Перемещение по Z": {
        "Русский": "Перемещение $z$",
        "Английский": "Displacement $z$",
    },
    "Удлинение": {
        "Русский": r"Удлинение $\Delta l$",
        "Английский": r"Elongation $\Delta l$",
    },
    "Удлинение по X": {
        "Русский": r"Удлинение $\Delta l_x$",
        "Английский": r"Elongation $\Delta l_x$",
    },
    "Удлинение по Y": {
        "Русский": r"Удлинение $\Delta l_y$",
        "Английский": r"Elongation $\Delta l_y$",
    },
    "Удлинение по Z": {
        "Русский": r"Удлинение $\Delta l_z$",
        "Английский": r"Elongation $\Delta l_z$",
    },
    "Деформация": {
        "Русский": r"Деформация $\varepsilon$",
        "Английский": r"Strain $\varepsilon$",
    },
    "Пластическая деформация": {
        "Русский": r"Пластическая деформация $\varepsilon_p$",
        "Английский": r"Plastic strain $\varepsilon_p$",
    },
    "Сила": {
        "Русский": "Сила $F$",
        "Английский": "Force $F$",
    },
    "Продольная сила": {
        "Русский": "Продольная сила $N$",
        "Английский": "Axial force $N$",
    },
    "Поперечная сила": {
        "Русский": "Поперечная сила $Q$",
        "Английский": "Shear force $Q$",
    },
    "Поперечная сила по Y": {
        "Русский": "Поперечная сила $Q_y$",
        "Английский": "Shear force $Q_y$",
    },
    "Поперечная сила по Z": {
        "Русский": "Поперечная сила $Q_z$",
        "Английский": "Shear force $Q_z$",
    },
    "Масса": {
        "Русский": "Масса $m$",
        "Английский": "Mass $m$",
    },
    "Напряжение": {
        "Русский": r"Напряжение $\sigma$",
        "Английский": r"Stress $\sigma$",
    },
    "Интенсивность напряжений": {
        "Русский": r"Интенсивность напряжений $\sigma_i$",
        "Английский": r"Stress intensity $\sigma_i$",
    },
    "Нормальное напряжение X": {
        "Русский": r"Нормальное напряжение $\sigma_x$",
        "Английский": r"Normal stress $\sigma_x$",
    },
    "Нормальное напряжение Y": {
        "Русский": r"Нормальное напряжение $\sigma_y$",
        "Английский": r"Normal stress $\sigma_y$",
    },
    "Нормальное напряжение Z": {
        "Русский": r"Нормальное напряжение $\sigma_z$",
        "Английский": r"Normal stress $\sigma_z$",
    },
    "Касательное напряжение XY": {
        "Русский": r"Касательное напряжение $\tau_{xy}$",
        "Английский": r"Shear stress $\tau_{xy}$",
    },
    "Касательное напряжение XZ": {
        "Русский": r"Касательное напряжение $\tau_{xz}$",
        "Английский": r"Shear stress $\tau_{xz}$",
    },
    "Касательное напряжение YX": {
        "Русский": r"Касательное напряжение $\tau_{yx}$",
        "Английский": r"Shear stress $\tau_{yx}$",
    },
    "Касательное напряжение YZ": {
        "Русский": r"Касательное напряжение $\tau_{yz}$",
        "Английский": r"Shear stress $\tau_{yz}$",
    },
    "Касательное напряжение ZX": {
        "Русский": r"Касательное напряжение $\tau_{zx}$",
        "Английский": r"Shear stress $\tau_{zx}$",
    },
    "Касательное напряжение ZY": {
        "Русский": r"Касательное напряжение $\tau_{zy}$",
        "Английский": r"Shear stress $\tau_{zy}$",
    },
    "Крутящий момент Mx": {
        "Русский": "Крутящий момент $M_x$",
        "Английский": "Torque $M_x$",
    },
    "Изгибающий момент Mx": {
        "Русский": "Изгибающий момент $M_x$",
        "Английский": "Bending moment $M_x$",
    },
    "Изгибающий момент My": {
        "Русский": "Изгибающий момент $M_y$",
        "Английский": "Bending moment $M_y$",
    },
    "Изгибающий момент Mz": {
        "Русский": "Изгибающий момент $M_z$",
        "Английский": "Bending moment $M_z$",
    },
    "Частота 1": {
        "Русский": "Частота ${{f}}_{{\\mathit{1}}}$",
        "Английский": "Frequency ${{f}}_{{\\mathit{1}}}$",
    },
    "Частота 2": {
        "Русский": "Частота ${{f}}_{{\\mathit{2}}}$",
        "Английский": "Frequency ${{f}}_{{\\mathit{2}}}$",
    },
    "Частота 3": {
        "Русский": "Частота ${{f}}_{{\\mathit{3}}}$",
        "Английский": "Frequency ${{f}}_{{\\mathit{3}}}$",
    },
}


class TitleProcessor:
    def __init__(self, combo_title, combo_size=None, entry_title=None, language="Русский"):
        self.combo_title = combo_title
        self.combo_size = combo_size
        self.entry_title = entry_title
        self.language = language

    def _get_units(self):
        if self.combo_size is None:
            return ""
        unit = self.combo_size.get()
        if unit in ("", "—"):
            return ""
        return f", {unit}"

    def _get_title(self):
        selection = self.combo_title.get()
        return title_mapping.get(selection, {}).get(self.language, selection)

    def get_processed_title(self):
        selection = self.combo_title.get()
        if selection in ("Другое", ""):
            return self.entry_title.get() if self.entry_title else ""
        if selection == "Нет":
            return ""
        title = self._get_title()
        return f"{title}{self._get_units()}"

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
):

    # Очистка предыдущего графика
    ax.clear()
    language = combo_language.get() or "Русский"
    title_processor = TitleProcessor(combo_title, entry_title=entry_title_custom, language=language)
    xlabel_processor = TitleProcessor(
        combo_titleX, combo_titleX_size, entry_titleX, language
    )
    ylabel_processor = TitleProcessor(
        combo_titleY, combo_titleY_size, entry_titleY, language
    )
    title = title_processor.get_processed_title()
    xlabel = xlabel_processor.get_processed_title()
    ylabel = ylabel_processor.get_processed_title()

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
        curves_info.append(curve_info)

    create_plot(
        curves_info, xlabel, ylabel, title, fig=fig, ax=ax, legend=legend_checkbox.get()
    )

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
