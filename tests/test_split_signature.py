from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import MathTextParser

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.title_utils import format_signature


parser = MathTextParser('agg')


def test_format_signature_basic():
    result = format_signature('Угол α', bold=False)
    parser.parse(result.replace('\\upalpha', '\\alpha'))
    assert result == 'Угол $\\upalpha$'


def test_format_signature_bold():
    result = format_signature('Момент M_x', bold=True)
    parser.parse(result)
    assert result == r"\textbf{Момент }$\boldsymbol{\mathit{M}_{\mathit{x}}}$"


def test_format_signature_roundtrip():
    text = 'Сила F_x'
    formatted = format_signature(text, bold=True)
    parser.parse(formatted)
    assert formatted == r"\textbf{Сила }$\boldsymbol{\mathit{F}_{\mathit{x}}}$"

