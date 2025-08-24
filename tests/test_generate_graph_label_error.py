import matplotlib.pyplot as plt
import pytest

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


def test_generate_graph_invalid_label_markup():
    fig, ax = plt.subplots()
    canvas = DummyCanvas()
    combo_title = Dummy("Нет")
    entry_title_custom = Dummy("")
    combo_titleX = Dummy("Другое")
    combo_titleX_size = Dummy("")
    entry_titleX = Dummy("$invalid")
    combo_titleY = Dummy("Другое")
    combo_titleY_size = Dummy("")
    entry_titleY = Dummy("y")
    legend_checkbox = Dummy(False)
    curves_frame = DummyFrame()
    combo_curves = Dummy("0")
    combo_language = Dummy("Русский")
    legend_title_combo = Dummy("Нет")
    legend_title_entry = Dummy("")
    legend_title_var = Dummy("Нет")

    with pytest.raises(ValueError) as excinfo:
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
            legend_title_var,
        )
    plt.close(fig)
    assert "неправильной разметкой подписи" in str(excinfo.value)
