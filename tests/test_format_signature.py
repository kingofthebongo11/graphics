from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import MathTextParser
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.title_utils import format_signature


parser = MathTextParser('agg')


def _parse_or_fail(text: str) -> None:
    try:
        parser.parse(text)
    except Exception as exc:  # pragma: no cover - явное сообщение при ошибке
        pytest.fail(f"Ошибка парсинга '{text}': {exc}")


def test_latin_italic():
    result = format_signature('Момент M_x', bold=False)
    _parse_or_fail(result)
    assert result == 'Момент $\\mathit{M}_{\\mathit{x}}$'


def test_greek_upright():
    result = format_signature('Угол α', bold=False)
    _parse_or_fail(result.replace('\\upalpha', '\\alpha'))
    assert result == 'Угол $\\upalpha$'


def test_bold_true():
    result = format_signature('Сила F_x', bold=True)
    _parse_or_fail(result)
    assert result == r"\textbf{Сила }$\boldsymbol{\mathit{F}_{\mathit{x}}}$"


def test_no_nested_dollars_existing_indices():
    text = 'Касательное напряжение \\uptau_{\\mathit{x}\\mathit{y}}'
    result = format_signature(text, bold=False)
    _parse_or_fail(result.replace('\\uptau', '\\tau'))
    assert result == 'Касательное напряжение $\\uptau_{\\mathit{x}\\mathit{y}}$'
