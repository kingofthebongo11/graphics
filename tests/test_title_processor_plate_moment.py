from matplotlib.mathtext import MathTextParser

from tabs.functions_for_tab1.plotting import TitleProcessor
from tabs.constants import TITLE_TRANSLATIONS
from tabs.title_utils import format_signature


class ComboStub:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


def test_plate_moment_title_and_unit():
    title_combo = ComboStub("Изгибающий момент Mx(п)")
    size_combo = ComboStub("Н·м/м")
    processor = TitleProcessor(
        title_combo,
        combo_size=size_combo,
        language="Русский",
        translations=TITLE_TRANSLATIONS,
    )
    joined = processor.get_processed_title()
    expected_plain = (
        f"{TITLE_TRANSLATIONS['Изгибающий момент Mx(п)']['Русский']}, Н·м/м"
    )
    assert joined == format_signature(expected_plain, bold=False)
    parser = MathTextParser("agg")
    parser.parse(joined)

