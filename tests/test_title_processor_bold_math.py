from matplotlib.mathtext import MathTextParser

from tabs.functions_for_tab1.plotting import TitleProcessor
from tabs.constants import TITLE_TRANSLATIONS
from tabs.title_utils import format_signature


class ComboStub:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


def test_title_processor_wraps_mathit_with_bold():
    combo_title = ComboStub("Время")
    processor = TitleProcessor(combo_title, bold_math=True)
    joined = processor.get_processed_title()
    expected = format_signature(TITLE_TRANSLATIONS["Время"]["Русский"], bold=True)
    assert joined == expected
    assert r"\textbf" in joined
    parser = MathTextParser("agg")
    parser.parse(joined)


def test_title_processor_uses_bold_dict_only_for_title():
    combo = ComboStub("Время")
    title_proc = TitleProcessor(combo, bold_math=True)
    axis_proc = TitleProcessor(combo, translations=TITLE_TRANSLATIONS)
    joined_title = title_proc.get_processed_title()
    joined_axis = axis_proc.get_processed_title()
    expected_plain = TITLE_TRANSLATIONS["Время"]["Русский"]
    assert joined_title == format_signature(expected_plain, bold=True)
    assert joined_axis == format_signature(expected_plain, bold=False)
    parser = MathTextParser("agg")
    parser.parse(joined_title)
    parser.parse(joined_axis)


def test_title_processor_wraps_multiple_mathit_occurrences():
    combo_title = ComboStub("Другое")
    entry = ComboStub("Value $\\mathit{x}+\\mathit{y}$")
    processor = TitleProcessor(combo_title, entry_title=entry, bold_math=True)
    joined = processor.get_processed_title()
    expected = format_signature(entry.get(), bold=True)
    assert joined == expected
    parser = MathTextParser("agg")
    parser.parse(joined)


def test_title_processor_wraps_M_symbols_and_preserves_math():
    combo_title = ComboStub("Другое")
    entry = ComboStub("M_x My $M_z$ $v$ \\boldsymbol{My}")
    processor = TitleProcessor(combo_title, entry_title=entry, bold_math=True)
    joined = processor.get_processed_title()
    expected = format_signature(entry.get(), bold=True)
    assert joined == expected
    parser = MathTextParser("agg")
    parser.parse(joined)

