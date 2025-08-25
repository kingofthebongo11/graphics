import importlib.util
from pathlib import Path

import pytest
from PIL import Image

if importlib.util.find_spec("docx") is None:  # pragma: no cover - зависимость
    pytest.skip("python-docx не установлен", allow_module_level=True)

from docx import Document
from report_docx import _format_section_title, build_report


def _make_png(path: Path) -> None:
    Image.new("RGB", (1, 1), color="white").save(path)


def test_format_section_title_strips_prefix():
    assert _format_section_title("01-Test") == "Test"
    assert _format_section_title("02-Name-Extra") == "Name (Extra)"


def test_build_report_orders_sections(tmp_path: Path):
    folders = ["10-Ten", "2-Two", "01-One"]
    for name in folders:
        d = tmp_path / name
        d.mkdir()
        _make_png(d / "img.png")

    docx_path = build_report(tmp_path)
    headings = [p.text for p in Document(docx_path).paragraphs if p.style.name == "Heading 1"]

    assert headings == ["One", "Two", "Ten"]
    assert all(not any(ch.isdigit() for ch in h) for h in headings)
