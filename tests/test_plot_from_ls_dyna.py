from pathlib import Path
from unittest.mock import patch

from analysis_types import AnalysisType
from plot_from_txt import plot_from_txt
from PIL import Image


def _fake_create_plot(curves_info, x_label, y_label, title, save_file, file_plt, **kwargs):
    Image.new("RGB", (1, 1), color="white").save(file_plt)


def test_plot_from_ls_dyna(tmp_path):
    txt_file = (
        Path(__file__).resolve().parents[1]
        / "examples"
        / "LsDynaText"
        / "LsDyna_example.txt"
    )
    output = tmp_path / "curve.png"
    with patch("plot_from_txt.create_plot", side_effect=_fake_create_plot):
        result = plot_from_txt(
            str(txt_file), AnalysisType.TIME_AXIAL_FORCE.value, str(output)
        )
    assert output.exists()
    assert result == str(output)
