from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.title_utils import split_signature, format_signature


def join(parts):
    return ''.join(f'${frag}$' if is_latex else frag for frag, is_latex in parts)


def test_split_signature_basic():
    parts = split_signature('Угол α', bold=False)
    assert parts == [('Угол ', False), ('\\upalpha', True)]


def test_split_signature_bold():
    parts = split_signature('Момент M_x', bold=True)
    assert parts == [
        ('\\textbf{Момент }', False),
        ('\\boldsymbol{\\mathit{M}_{\\mathit{x}}}', True),
    ]


def test_split_signature_roundtrip():
    text = 'Сила F_x'
    parts = split_signature(text, bold=True)
    assert join(parts) == format_signature(text, bold=True)
