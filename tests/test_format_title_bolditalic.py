from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import MathTextParser

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.title_utils import bold_math_symbols, format_title_bolditalic


def test_format_title_bolditalic_with_pre_bold_math():
    text = r"Время $\boldsymbol{\mathit{t}}$"
    processed = bold_math_symbols(text)
    formatted = format_title_bolditalic(processed)
    parser = MathTextParser('agg')
    parser.parse(formatted)


