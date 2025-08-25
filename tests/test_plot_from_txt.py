from pathlib import Path
from unittest.mock import patch

from plot_from_txt import extract_labels, plot_from_txt
from analysis_types import AnalysisType


def test_extract_labels():
    x, y, title = extract_labels(AnalysisType.TIME_AXIAL_FORCE.value)
    assert x == "Время $\\mathit{\\mathit{t}}$, с"
    assert y == "Продольная сила $\\mathit{\\mathit{N}}$, Н"
    assert title == y


def test_plot_from_txt(tmp_path):
    data = "0 0\n1 1\n"
    txt_file = tmp_path / "data.txt"
    txt_file.write_text(data, encoding="utf-8")
    out_file = tmp_path / "out.png"

    def fake_create_plot(curves_info, x_label, y_label, title, save_file, file_plt, **kwargs):
        Path(file_plt).touch()

    with patch("plot_from_txt.create_plot", side_effect=fake_create_plot) as mocked:
        result = plot_from_txt(str(txt_file), AnalysisType.TIME_AXIAL_FORCE.value, str(out_file))
        mocked.assert_called_once()
    assert Path(result).exists()
