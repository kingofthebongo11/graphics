import matplotlib.pyplot as plt
from unittest.mock import patch
import pytest

from tabs.functions_for_tab1.plotting import generate_graph
from tabs.constants import LEGEND_TITLE_TRANSLATIONS


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


@pytest.mark.parametrize(
    "language, option",
    [
        ("Русский", "№ Элементов"),
        ("Английский", "№ Элементов"),
        ("Русский", "№ Узлов"),
        ("Английский", "№ Узлов"),
    ],
)
def test_generate_graph_legend_title_translations(language, option):
    fig, ax = plt.subplots()
    canvas = DummyCanvas()
    combo_title = Dummy("Нет")
    entry_title_custom = Dummy("")
    combo_titleX = Dummy("Нет")
    combo_titleX_size = Dummy("")
    entry_titleX = Dummy("")
    combo_titleY = Dummy("Нет")
    combo_titleY_size = Dummy("")
    entry_titleY = Dummy("")
    legend_checkbox = Dummy(True)
    curves_frame = DummyFrame()
    combo_curves = Dummy("0")
    combo_language = Dummy(language)
    selection = LEGEND_TITLE_TRANSLATIONS[option][language]
    legend_title_combo = Dummy(selection)
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

    legend = ax.get_legend()
    assert legend.get_title().get_text() == selection
    plt.close(fig)


@pytest.mark.parametrize("language", ["Русский", "Английский"])
def test_generate_graph_legend_title_custom(language):
    fig, ax = plt.subplots()
    canvas = DummyCanvas()
    combo_title = Dummy("Нет")
    entry_title_custom = Dummy("")
    combo_titleX = Dummy("Нет")
    combo_titleX_size = Dummy("")
    entry_titleX = Dummy("")
    combo_titleY = Dummy("Нет")
    combo_titleY_size = Dummy("")
    entry_titleY = Dummy("")
    legend_checkbox = Dummy(True)
    curves_frame = DummyFrame()
    combo_curves = Dummy("0")
    combo_language = Dummy(language)
    selection = LEGEND_TITLE_TRANSLATIONS["Другое"][language]
    legend_title_combo = Dummy(selection)
    custom_text = "My legend" if language == "Английский" else "Моя легенда"
    legend_title_entry = Dummy(custom_text)

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

    legend = ax.get_legend()
    assert legend.get_title().get_text() == custom_text
    plt.close(fig)
