import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from unittest.mock import patch

from tabs.function_for_all_tabs.plotting import create_plot
from tabs.title_utils import split_signature


def test_segments_usetex_and_font():
    fig, ax = plt.subplots()
    curves = [{"X_values": [0, 1], "Y_values": [0, 1]}]
    title = split_signature("Title M_x", bold=False)
    with patch(
        "matplotlib.text.Text.get_window_extent",
        return_value=Bbox.from_bounds(0, 0, 1, 1),
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
