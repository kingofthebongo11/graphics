from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import MathTextParser
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.title_utils import split_signature


def join_segments(parts):
    return "".join(f"${frag}$" if is_latex else frag for frag, is_latex in parts)

parser = MathTextParser('agg')


def _parse_or_fail(text: str) -> None:
    try:
        parser.parse(text)
    except Exception as exc:  # pragma: no cover - явное сообщение при ошибке
        pytest.fail(f"Ошибка парсинга '{text}': {exc}")


def test_latin_italic():
    parts = split_signature('Момент M_x', bold=False)
    result = join_segments(parts)
    _parse_or_fail(result)
    assert parts == [('Момент ', False), ('\\mathit{M}_{\\mathit{x}}', True)]


def test_greek_upright():
    parts = split_signature('Угол α', bold=False)
    assert parts == [('Угол ', False), ('\\upalpha', True)]


def test_bold_true():
    parts = split_signature('Сила F_x', bold=True)
    result = join_segments(parts)
    _parse_or_fail(result)
    assert ('\\boldsymbol{\\mathit{F}_{\\mathit{x}}}', True) in parts
