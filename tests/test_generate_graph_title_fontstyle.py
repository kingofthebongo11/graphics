import shutil
from unittest.mock import patch

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pytest

from tabs.functions_for_tab1.plotting import generate_graph
from tabs.function_for_all_tabs.plotting import TITLE_SIZE, LABEL_SIZE


class Dummy:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value


class DummyCanvas:
    def draw(self):
        pass


class DummyFrame:
    def winfo_children(self):
        return []


@pytest.mark.skipif(shutil.which("latex") is None, reason="LaTeX not installed")
def test_generate_graph_title_fontstyle_normal():
    fig, ax = plt.subplots()
    canvas = DummyCanvas()
    combo_title = Dummy("Время")
    entry_title_custom = Dummy("")
    combo_titleX = Dummy("Нет")
    combo_titleX_size = Dummy("")
    entry_titleX = Dummy("")
    combo_titleY = Dummy("Нет")
    combo_titleY_size = Dummy("")
    entry_titleY = Dummy("")
    legend_checkbox = Dummy(False)
    curves_frame = DummyFrame()
    combo_curves = Dummy("0")
    combo_language = Dummy("Русский")
    legend_title_combo = Dummy("Нет")
    legend_title_entry = Dummy("")

    with patch("tabs.function_for_all_tabs.plotting.configure_matplotlib", lambda: None):
        plt.rcParams.update({"text.usetex": False})
        generate_graph(
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
        )

    expected_title_size = FontProperties(size=TITLE_SIZE).get_size_in_points()
    expected_label_size = FontProperties(size=LABEL_SIZE).get_size_in_points()
    assert ax.title.get_fontstyle() == "normal"
    assert ax.title.get_fontsize() == expected_title_size
    assert ax.xaxis.label.get_fontsize() == expected_label_size
    assert ax.yaxis.label.get_fontsize() == expected_label_size
    plt.close(fig)
