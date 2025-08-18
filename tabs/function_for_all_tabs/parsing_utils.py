from pathlib import Path
from typing import List, Tuple

from tabs.functions_for_tab1.curves_from_file.text_file import read_X_Y_from_text_file


def read_pairs(path: str) -> Tuple[List[float], List[float]]:
    """Read X and Y value pairs from a text file.

    This function is a thin adapter over
    :func:`tabs.functions_for_tab1.curves_from_file.text_file.read_X_Y_from_text_file`.
    It delegates parsing to the existing implementation and simply returns the
    extracted arrays of X and Y values.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(path)

    curve_info = {"curve_file": str(path_obj)}
    read_X_Y_from_text_file(curve_info)
    try:
        return curve_info["X_values"], curve_info["Y_values"]
    except KeyError as exc:
        raise ValueError("Некорректные данные в файле") from exc
