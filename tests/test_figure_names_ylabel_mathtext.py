from matplotlib.mathtext import MathTextParser
import pytest

from tabs.functions_for_tab3.Figurenameclass import FigureNames

parser = MathTextParser("agg")

@pytest.mark.parametrize("axis", ["X", "Y", "Z", "XR", "YR", "ZR"])
def test_generate_plot_ylabel_mathtext_parsable(axis):
    label = FigureNames(f"{axis}eig").generate_plot_ylabel()
    try:
        parser.parse(label)
    except Exception as exc:  # pragma: no cover - explicit message on failure
        pytest.fail(f"Ошибка парсинга подписи '{label}': {exc}")
