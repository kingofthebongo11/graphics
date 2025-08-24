import pytest
from tabs.tab1 import on_combo_changeX_Y_labels
from tabs.constants import UNITS_MAPPING, DEFAULT_UNITS


class ComboStub:
    def __init__(self, selection):
        self._selection = selection
    def get(self):
        return self._selection
    def winfo_x(self):
        return 0
    def winfo_y(self):
        return 0


class EntryStub:
    placed = False

    def place(self, *args, **kwargs):
        self.placed = True

    def place_forget(self):
        self.placed = False


class LabelStub:
    def place(self, *args, **kwargs):
        pass
    def place_forget(self):
        pass


class SizeComboStub:
    def __init__(self):
        self.values = []
        self.current_index = None
        self.placed = False
    def __setitem__(self, key, value):
        if key == "values":
            self.values = value
    def set(self, value):
        pass
    def place(self, *args, **kwargs):
        self.placed = True

    def place_forget(self):
        self.placed = False
    def current(self, index):
        self.current_index = index
    def winfo_x(self):
        return 0
    def winfo_y(self):
        return 0


def _call(selection):
    combo = ComboStub(selection)
    entry = EntryStub()
    label = LabelStub()
    size_combo = SizeComboStub()
    size_entry = EntryStub()
    on_combo_changeX_Y_labels(combo, entry, label, size_combo, size_entry)
    return size_combo.values, size_combo.current_index


@pytest.mark.parametrize(
    "selection",
    [
        "Пластическая деформация",
        "Интенсивность пластических деформаций",
        "Интенсивность напряжений",
        "Сила",
        "Удлинение по X",
        "Крутящий момент Mx",
        "Изгибающий момент Ms (My)",
        "Изгибающий момент My",
        "Изгибающий момент Mt (Mz)",
        "Изгибающий момент Mz",
    ],
)
def test_units_for_new_physical_quantities(selection):
    values, index = _call(selection)
    expected_values = UNITS_MAPPING[selection]
    expected_index = expected_values.index(DEFAULT_UNITS[selection])
    assert values == expected_values
    assert index == expected_index
    assert values[0] == "Нет"
    assert values[-1] == "Другое"
