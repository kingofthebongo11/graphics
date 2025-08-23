from matplotlib.mathtext import MathTextParser

from tabs.functions_for_tab1.plotting import TitleProcessor
from tabs.constants import TITLE_TRANSLATIONS


class ComboStub:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


def test_title_processor_wraps_mathit_with_bold():
    combo_title = ComboStub("Время")
    processor = TitleProcessor(combo_title, bold_math=True)
    result = processor.get_processed_title()
    joined = "".join(
        f"${frag}$" if is_latex else frag for frag, is_latex in result
    )
    assert r"\boldsymbol{\mathit{t}}" in joined
    assert r"\textbf" not in joined
    parser = MathTextParser("agg")
    parser.parse(joined)


def test_title_processor_uses_bold_dict_only_for_title():
    combo = ComboStub("Время")
    title_proc = TitleProcessor(combo, bold_math=True)
    axis_proc = TitleProcessor(combo, translations=TITLE_TRANSLATIONS)
    joined_title = "".join(
        f"${frag}$" if is_latex else frag
        for frag, is_latex in title_proc.get_processed_title()
    )
    joined_axis = "".join(
        f"${frag}$" if is_latex else frag
        for frag, is_latex in axis_proc.get_processed_title()
    )
    assert r"\boldsymbol{\mathit{t}}" in joined_title
    assert r"\boldsymbol{\mathit{t}}" not in joined_axis


def test_title_processor_wraps_multiple_mathit_occurrences():
    combo_title = ComboStub("Другое")
    entry = ComboStub("Value $\\mathit{x}+\\mathit{y}$")
    processor = TitleProcessor(combo_title, entry_title=entry, bold_math=True)
    result = processor.get_processed_title()
    joined = "".join(
        f"${frag}$" if is_latex else frag for frag, is_latex in result
    )
    assert joined.count(r"\boldsymbol{\mathit{") == 2
    parser = MathTextParser("agg")
    parser.parse(joined)


def test_title_processor_wraps_M_symbols_and_preserves_math():
    combo_title = ComboStub("Другое")
    entry = ComboStub("M_x My $M_z$ $v$ \\boldsymbol{My}")
    processor = TitleProcessor(combo_title, entry_title=entry, bold_math=True)
    result = processor.get_processed_title()
    joined = "".join(
        f"${frag}$" if is_latex else frag for frag, is_latex in result
    )
    assert r"\boldsymbol{\mathit{M}_{\mathit{x}}}" in joined
    assert joined.count(r"\boldsymbol{My}") == 1
    assert " My " in joined
    assert "$\\boldsymbol{\mathit{M}_{\mathit{z}}}$" in joined
    assert "$\\boldsymbol{\mathit{v}}$" in joined
    parser = MathTextParser("agg")
    parser.parse(joined)
