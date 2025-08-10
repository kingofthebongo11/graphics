import numpy as np
from tkinter import filedialog, messagebox

from tabs.function_for_all_tabs import create_plot
from .curves_from_file import (
    read_X_Y_from_frequency_analysis,
    read_X_Y_from_text_file,
    read_X_Y_from_ls_dyna,
    read_X_Y_from_excel,
)


class AxisTitleProcessor:
    def __init__(self, combo_title, combo_size, language='Русский'):
        self.combo_title = combo_title
        self.combo_size = combo_size
        self.language = language
        self.title_mapping = {
            "Время": {
                "Русский": "Время $t$",
                "Английский": "Time $t$",
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

    def _get_units(self):
        units = {
            "Время": {
                "Русский": "с",
                "Английский": "s",
            },
            "Частота 1": {
                "Русский": "Гц",
                "Английский": "Hz",
            },
            "Частота 2": {
                "Русский": "Гц",
                "Английский": "Hz",
            },
            "Частота 3": {
                "Русский": "Гц",
                "Английский": "Hz",
            },
        }
        selection = self.combo_title.get()
        unit = units.get(selection, {}).get(self.language, "")
        return f", {unit}" if unit else ""

    def _get_title(self):
        selection = self.combo_title.get()
        return self.title_mapping.get(selection, {}).get(self.language, selection)

    def get_processed_title(self):
        if self.combo_title.get() == "Другое" and self.combo_size.get():
            return f"{self.combo_size.get()}"
        title = self._get_title()
        return f"{title}{self._get_units()}"


def save_file(entry_widget, graph_info):

    file_name = entry_widget.get()
    if file_name:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                                 initialfile=file_name)
        if file_path:
            try:
                curves_info = [{
                    'X_values': graph_info['X_values'],
                    'Y_values': graph_info['Y_values']
                }]
                create_plot(curves_info, graph_info['X_label'], graph_info['Y_label'], graph_info['title'],
                            savefile=True,
                            file_plt=file_path)  # Генерация и сохранение графика
                messagebox.showinfo("Успех", f"График сохранен: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    else:
        messagebox.showerror("Ошибка", "Имя файла не может быть пустым!")


def get_X_Y_data(curve_info):
    if curve_info['curve_type'] == 'Частотный анализ':
        read_X_Y_from_frequency_analysis(curve_info)
    elif curve_info['curve_type'] == 'Текстовой файл':
        read_X_Y_from_text_file(curve_info)
    elif curve_info['curve_type'] == 'Файл кривой LS-Dyna':
        read_X_Y_from_ls_dyna(curve_info)
    elif curve_info['curve_type'] == 'Excel файл':
        read_X_Y_from_excel(curve_info)


def generate_graph(ax, fig, canvas, path_entry_title, combo_titleX, combo_titleX_size, combo_titleY, combo_titleY_size,
                   legend_checkbox, curves_frame, combo_curves, combo_language):

    # Очистка предыдущего графика
    ax.clear()
    # Считываем заголовок из поля ввода
    title = path_entry_title.get()
    language = combo_language.get() or 'Русский'
    xlabel_processor = AxisTitleProcessor(combo_titleX, combo_titleX_size, language)
    ylabel_processor = AxisTitleProcessor(combo_titleY, combo_titleY_size, language)
    xlabel = xlabel_processor.get_processed_title()
    ylabel = ylabel_processor.get_processed_title()

    # Считываем количество кривых из combobox
    num_curves = int(combo_curves.get())

    # Генерация данных для графика (пример - синусоида)
    x = np.linspace(0, 10, 100)
    curves_info = []
    # Построение каждой кривой в цикле
    for i in range(1, num_curves + 1):
        curve_info = {}
        for widget in curves_frame.winfo_children():
            if hasattr(widget, '_name'):
                widget_name = widget._name

                # Проверяем тип кривой
                if widget_name == f"curve_{i}_type":
                    curve_info['curve_type'] = widget.get()

                # Если тип кривой "Частотный анализ", собираем дополнительные данные
                if 'curve_type' in curve_info and curve_info['curve_type'] == "Частотный анализ":
                    if widget_name == f"curve_{i}_typeXF":
                        curve_info['curve_typeXF'] = widget.get()
                    elif widget_name == f"curve_{i}_typeYF":
                        curve_info['curve_typeYF'] = widget.get()
                    elif widget_name == f"curve_{i}_typeXFtype":
                        curve_info['curve_typeXF_type'] = widget.get()
                    elif widget_name == f"curve_{i}_typeYFtype":
                        curve_info['curve_typeYF_type'] = widget.get()

                # Получаем имя файла для каждой кривой
                if widget_name == f"curve_{i}_filename":
                    curve_info['curve_file'] = widget.get()

                if widget_name == f"curve_{i}_horizontal":
                    curve_info['horizontal'] = widget.var.get()
                elif widget_name == f"curve_{i}_X_range":
                    curve_info['X_range'] = widget.get()
                elif widget_name == f"curve_{i}_Y_range":
                    curve_info['Y_range'] = widget.get()

                # Проверяем наличие легенды, если отмечен чекбокс
                if legend_checkbox.get() and widget_name == f"curve_{i}_legend":
                    curve_info['curve_legend'] = widget.get()

        # Добавляем информацию о кривой в общий список
        get_X_Y_data(curve_info)
        curves_info.append(curve_info)

    create_plot(curves_info, xlabel, ylabel, title,
                fig=fig, ax=ax, legend=legend_checkbox.get())

    # Перерисовка графика
    canvas.draw()
