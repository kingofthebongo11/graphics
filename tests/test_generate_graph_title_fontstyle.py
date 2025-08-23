import matplotlib.pyplot as plt
from unittest.mock import patch

from tabs.functions_for_tab1.plotting import generate_graph


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

    captured = {}

    def fake_create_plot(curves_info, x_label, y_label, title, **kwargs):
        captured["title_fontstyle"] = kwargs.get("title_fontstyle")

    with patch("tabs.functions_for_tab1.plotting.create_plot", fake_create_plot):
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
        )
    plt.close(fig)
    assert captured.get("title_fontstyle") == "normal"
