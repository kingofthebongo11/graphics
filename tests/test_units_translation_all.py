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
        ("Время", [(ru, en) for ru, en in TIME_UNIT_PAIRS if ru != "Нет"]),
        (
            "Перемещение по X",
            [(ru, en) for ru, en in LENGTH_UNIT_PAIRS if ru != "Нет"],
        ),
        (
            "Деформация",
            [(ru, en) for ru, en in DEFORMATION_UNIT_PAIRS if ru != "Нет"],
        ),
        ("Сила", [(ru, en) for ru, en in FORCE_UNIT_PAIRS if ru != "Нет"]),
        ("Масса", [(ru, en) for ru, en in MASS_UNIT_PAIRS if ru != "Нет"]),
        (
            "Напряжение",
            [(ru, en) for ru, en in STRESS_UNITS_PAIRS if ru != "Нет"],
        ),
        (
            "Крутящий момент Mx",
            [(ru, en) for ru, en in MOMENT_UNIT_PAIRS if ru != "Нет"],
        ),
        (
            "Частота 1",
            [(ru, en) for ru, en in FREQUENCY_UNIT_PAIRS if ru != "Нет"],
        ),
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
