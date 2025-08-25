from pathlib import Path
from unittest.mock import patch

from plot_from_txt import extract_labels, plot_from_txt, plot_from_txt_files
from analysis_types import AnalysisType
from tabs.constants import (
    DEFAULT_UNITS,
    LEGEND_TITLE_TRANSLATIONS,
    TITLE_TRANSLATIONS_BOLD,
)
from tabs.title_utils import format_signature


def test_extract_labels():
    x, y, title = extract_labels(AnalysisType.TIME_AXIAL_FORCE.value)
    assert x == "Время $\\mathit{\\mathit{t}}$, с"
    assert y == "Продольная сила $\\mathit{\\mathit{N}}$, Н"
    expected_title = format_signature(
        f"{TITLE_TRANSLATIONS_BOLD['Продольная сила']['Русский']}, {DEFAULT_UNITS['Продольная сила']}",
        bold=True,
    )
    assert title == expected_title


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


def test_plot_from_txt_files(tmp_path):
    top = tmp_path / "pilon-element-beam"
    analysis_dir = top / "analysis"
    analysis_dir.mkdir(parents=True)

    data = "0 0\n1 1\n"
    f1 = analysis_dir / "10.txt"
    f1.write_text(data, encoding="utf-8")
    f2 = analysis_dir / "20.txt"
    f2.write_text(data, encoding="utf-8")

    expected_legend = LEGEND_TITLE_TRANSLATIONS["№ Элементов"]["Русский"]

    def fake_create_plot(curves_info, x_label, y_label, title, legend, legend_title, save_file, file_plt, **kwargs):
        assert [c["curve_legend"] for c in curves_info] == ["10", "20"]
        assert legend is True
        assert legend_title == expected_legend
        Path(file_plt).touch()

    with patch("plot_from_txt.create_plot", side_effect=fake_create_plot) as mocked:
        result = plot_from_txt_files([str(f1), str(f2)], AnalysisType.TIME_AXIAL_FORCE.value)
        mocked.assert_called_once()
    assert Path(result).exists()
