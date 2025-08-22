from matplotlib.mathtext import MathTextParser

from tabs.functions_for_tab1.plotting import TitleProcessor


class ComboStub:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


def test_title_processor_wraps_mathit_with_bold():
    combo_title = ComboStub("Время")
    processor = TitleProcessor(combo_title, bold_math=True)
    result = processor.get_processed_title()
    assert "\\mathbf{\\mathit{t}}" in result
    parser = MathTextParser("agg")
    parser.parse(result)


def test_title_processor_wraps_multiple_mathit_occurrences():
    combo_title = ComboStub("Другое")
    entry = ComboStub("Value $\\mathit{x}+\\mathit{y}$")
    processor = TitleProcessor(combo_title, entry_title=entry, bold_math=True)
    result = processor.get_processed_title()
    assert result.count("\\mathbf{\\mathit{") == 2
    parser = MathTextParser("agg")
    parser.parse(result)
