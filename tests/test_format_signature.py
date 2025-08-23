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
    assert '\\mathit{M}' in result
    assert '_{\\mathit{x}}' in result


def test_greek_upright():
    result = format_signature('Угол α', bold=False)
    assert '\\upalpha' in result
    assert '\\mathit' not in result


def test_bold_true():
    result = format_signature('Сила F_x', bold=True)
    _parse_or_fail(result)
    assert '\\boldsymbol' in result
