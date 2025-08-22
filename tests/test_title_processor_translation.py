from tabs.functions_for_tab1.plotting import TitleProcessor


class ComboStub:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


def test_title_processor_translates_to_english():
    title_combo = ComboStub("Сила")
    size_combo = ComboStub("кН")
    processor = TitleProcessor(title_combo, combo_size=size_combo, language="Английский")
    result = processor.get_processed_title()
    assert "Force" in result
    assert ", kN" in result
