import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from unittest.mock import patch

from tabs.function_for_all_tabs.plotting import create_plot
from tabs.title_utils import split_signature


def test_segments_usetex_and_font():
    plt.rcParams.update({"text.usetex": False})
    fig, ax = plt.subplots()
    curves = [{"X_values": [0, 1], "Y_values": [0, 1]}]
    title = split_signature("Title M_x", bold=False)
    with patch(
        "matplotlib.text.Text.get_window_extent",
        return_value=Bbox.from_bounds(0, 0, 1, 1),
    ), patch(
        "tabs.function_for_all_tabs.plotting.configure_matplotlib",
        lambda: plt.rcParams.update({"text.usetex": False}),
    ):
        create_plot(
            curves,
            split_signature("X", bold=False),
            split_signature("Y", bold=False),
            title,
            fig=fig,
            ax=ax,
        )
    plain = next(t for t in ax.texts if t.get_text() == "Title ")
    latex = next(t for t in ax.texts if t.get_text() == "$\\mathit{M}_{\\mathit{x}}$")
    assert not plain.get_usetex()
    assert "Times New Roman" in plain.get_fontfamily()
    assert latex.get_usetex()
    plt.close(fig)


def test_x_label_is_centered():
    plt.rcParams.update({"text.usetex": False})
    fig, ax = plt.subplots()
    curves = [{"X_values": [0, 1], "Y_values": [0, 1]}]
    x_label = [("A", False), ("B", False)]
    y_label = split_signature("Y", bold=False)

    def fake_extent(self, renderer=None):
        widths = {"A": 10, "B": 20, "Y": 10}
        w = widths.get(self.get_text(), 10)
        return Bbox.from_bounds(0, 0, w, 1)

    with patch("matplotlib.text.Text.get_window_extent", fake_extent), patch(
        "tabs.function_for_all_tabs.plotting.configure_matplotlib",
        lambda: plt.rcParams.update({"text.usetex": False}),
    ):
        create_plot(curves, x_label, y_label, [], fig=fig, ax=ax)

    a_text = next(t for t in ax.texts if t.get_text() == "A")
    b_text = next(t for t in ax.texts if t.get_text() == "B")
    w1 = b_text.get_position()[0] - a_text.get_position()[0]
    expected_start = 0.5 - 1.5 * w1
    assert abs(a_text.get_position()[0] - expected_start) < 1e-6
    plt.close(fig)


def test_y_label_is_centered_and_non_negative():
    plt.rcParams.update({"text.usetex": False})
    fig, ax = plt.subplots()
    curves = [{"X_values": [0, 1], "Y_values": [0, 1]}]
    x_label = split_signature("X", bold=False)
    y_label = [("A", False), ("B", False)]

    def fake_extent(self, renderer=None):
        heights = {"A": 10, "B": 20, "X": 10}
        h = heights.get(self.get_text(), 10)
        return Bbox.from_bounds(0, 0, 1, h)

    with patch("matplotlib.text.Text.get_window_extent", fake_extent), patch(
        "tabs.function_for_all_tabs.plotting.configure_matplotlib",
        lambda: plt.rcParams.update({"text.usetex": False}),
    ):
        create_plot(curves, x_label, y_label, [], fig=fig, ax=ax)

    a_text = next(t for t in ax.texts if t.get_text() == "A")
    b_text = next(t for t in ax.texts if t.get_text() == "B")
    h1 = a_text.get_position()[1] - b_text.get_position()[1]
    expected_start = 0.5 + 1.5 * h1
    assert abs(a_text.get_position()[1] - expected_start) < 1e-6
    assert a_text.get_position()[0] >= 0
    plt.close(fig)
