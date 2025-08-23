import pytest

from tabs.functions_for_tab1.plotting import TitleProcessor
from tabs.constants import (
    TITLE_TRANSLATIONS,
    TIME_UNIT_PAIRS,
    LENGTH_UNIT_PAIRS,
    DEFORMATION_UNIT_PAIRS,
    FORCE_UNIT_PAIRS,
    MASS_UNIT_PAIRS,
    STRESS_UNITS_PAIRS,
    MOMENT_UNIT_PAIRS,
    FREQUENCY_UNIT_PAIRS,
)


class ComboStub:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


@pytest.mark.parametrize(
    "quantity,pairs",
    [
        ("Время", TIME_UNIT_PAIRS),
        ("Перемещение по X", LENGTH_UNIT_PAIRS),
        ("Деформация", [(ru, en) for ru, en in DEFORMATION_UNIT_PAIRS if ru != "—"]),
        ("Сила", FORCE_UNIT_PAIRS),
        ("Масса", MASS_UNIT_PAIRS),
        ("Напряжение", STRESS_UNITS_PAIRS),
        ("Крутящий момент Mx", MOMENT_UNIT_PAIRS),
        ("Частота 1", FREQUENCY_UNIT_PAIRS),
    ],
)
def test_units_translation(quantity, pairs):
    for ru_unit, en_unit in pairs:
        combo_title = ComboStub(quantity)
        combo_size = ComboStub(ru_unit)
        processor = TitleProcessor(
            combo_title,
            combo_size=combo_size,
            language="Английский",
            translations=TITLE_TRANSLATIONS,
        )
        assert processor._get_units() == f", {en_unit}"
