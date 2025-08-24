from pathlib import Path
from unittest.mock import patch
import importlib.util
import pytest

from analysis_types import AnalysisType
from curves_pipeline import build_curves_report
from PIL import Image

if importlib.util.find_spec("docx") is None:
    pytest.skip("python-docx не установлен", allow_module_level=True)


def _fake_create_plot(curves_info, x_label, y_label, title, save_file, file_plt, **kwargs):
    Image.new("RGB", (1, 1), color="white").save(file_plt)


def test_build_curves_report(tmp_path):
    top = tmp_path / "Top"
    analysis_dir = top / AnalysisType.TIME_AXIAL_FORCE.value
    analysis_dir.mkdir(parents=True)
    txt_file = analysis_dir / "curve.txt"
    txt_file.write_text("0 0\n1 1\n", encoding="utf-8")

    with patch("plot_from_txt.create_plot", side_effect=_fake_create_plot):
        docx_path, errors = build_curves_report(tmp_path)

    assert not errors
    assert (analysis_dir / "curve.png").exists()
    assert docx_path is not None and docx_path.exists()
