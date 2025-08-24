import pytest
from tabs.tab1 import on_combo_changeX_Y_labels


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
    def place_forget(self):
        pass


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
        if key == 'values':
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
    on_combo_changeX_Y_labels(combo, entry, label, size_combo)
    return size_combo.values, size_combo.current_index


@pytest.mark.parametrize(
    "selection,expected_values,expected_index",
    [
        ("Пластическая деформация", ["%", "—"], 1),
        (
            "Интенсивность пластических деформаций",
            ["%", "—"],
            1,
        ),
        (
            "Интенсивность напряжений",
            [
                "МН/м²",
                "МН/мм²",
                "МН/см²",
                "МПа",
                "Н/м²",
                "Н/мм²",
                "Н/см²",
                "Па",
                "кН/м²",
                "кН/мм²",
                "кН/см²",
                "кПа",
                "кгс/м²",
                "кгс/мм²",
                "кгс/см²",
                "тс/м²",
                "тс/см²",
            ],
            7,
        ),
        ("Сила", ["Н", "кН", "кгс", "мН", "тс"], 0),
        ("Удлинение по X", ["м", "мм", "см"], 0),
        (
            "Крутящий момент Mx",
            ["Н·м", "кН·м", "кгс·м", "тс·м"],
            0,
        ),
        (
            "Изгибающий момент Ms (My)",
            ["Н·м", "кН·м", "кгс·м", "тс·м"],
            0,
        ),
        (
            "Изгибающий момент My",
            ["Н·м", "кН·м", "кгс·м", "тс·м"],
            0,
        ),
        (
            "Изгибающий момент Mt (Mz)",
            ["Н·м", "кН·м", "кгс·м", "тс·м"],
            0,
        ),
        (
            "Изгибающий момент Mz",
            ["Н·м", "кН·м", "кгс·м", "тс·м"],
            0,
        ),
    ],
)
def test_units_for_new_physical_quantities(selection, expected_values, expected_index):
    values, index = _call(selection)
    assert values == expected_values
    assert index == expected_index
