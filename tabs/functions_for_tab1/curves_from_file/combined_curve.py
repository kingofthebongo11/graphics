import logging
from .frequency_analysis import read_X_Y_from_frequency_analysis
from .text_file import read_X_Y_from_text_file
from .ls_dyna_file import read_X_Y_from_ls_dyna
from .excel_file import read_X_Y_from_excel

logger = logging.getLogger(__name__)


def _read_axis(axis_info, column=0):
    """Считывает данные для одной оси из указанного источника.

    Параметр ``column`` задаёт требуемую ось: ``0`` для X, ``1`` для Y.
    """
    source_type = axis_info.get("source")
    tmp_info = {"curve_file": axis_info.get("curve_file", "")}

    if source_type == "Частотный анализ":
        tmp_info.update({
            "curve_typeXF": axis_info.get("parameter", ""),
            "curve_typeYF": axis_info.get("parameter", ""),
            "curve_typeXF_type": axis_info.get("direction", ""),
            "curve_typeYF_type": axis_info.get("direction", ""),
        })
        read_X_Y_from_frequency_analysis(tmp_info)
        return tmp_info.get("X_values", []) if column == 0 else tmp_info.get("Y_values", [])

    if source_type == "Текстовой файл":
        read_X_Y_from_text_file(tmp_info)
        col = axis_info.get("column", column)
        return tmp_info.get("X_values", []) if col == 0 else tmp_info.get("Y_values", [])

    if source_type == "Файл кривой LS-Dyna":
        read_X_Y_from_ls_dyna(tmp_info)
        col = axis_info.get("column", column)
        return tmp_info.get("X_values", []) if col == 0 else tmp_info.get("Y_values", [])

    if source_type == "Excel файл":
        tmp_info.update({
            "horizontal": axis_info.get("horizontal", False),
            "use_offset": axis_info.get("use_offset", False),
            "offset_horizontal": axis_info.get("offset_horizontal", 0),
            "offset_vertical": axis_info.get("offset_vertical", 0),
            "use_ranges": axis_info.get("use_ranges", False),
            "range_x": axis_info.get("range_x", ""),
            "range_y": axis_info.get("range_y", ""),
        })
        read_X_Y_from_excel(tmp_info)
        return tmp_info.get("X_values", []) if column == 0 else tmp_info.get("Y_values", [])

    logger.error("Неизвестный источник данных: %s", source_type)
    return []


def read_X_Y_from_combined(curve_info):
    """Формирует точки (Xi, Yi) из разных источников данных.

    Ожидается, что в ``curve_info`` находятся два словаря ``X_source`` и
    ``Y_source`` с описанием источника для соответствующей оси.
    """

    x_vals = _read_axis(curve_info.get("X_source", {}), column=0)
    y_vals = _read_axis(curve_info.get("Y_source", {}), column=1)
    n = min(len(x_vals), len(y_vals))
    curve_info["X_values"] = x_vals[:n]
    curve_info["Y_values"] = y_vals[:n]
