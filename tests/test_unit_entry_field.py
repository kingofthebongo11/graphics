import pytest

from tabs.tab1 import on_unit_change


class ComboStub:
    def __init__(self, selection):
        self._selection = selection
        self.placed = True

    def get(self):
        return self._selection

    def place(self, *args, **kwargs):
        self.placed = True

    def place_forget(self):
        self.placed = False

    def winfo_x(self):
        return 0

    def winfo_y(self):
        return 0


class EntryStub:
    def __init__(self):
        self.placed = False

    def place(self, *args, **kwargs):
        self.placed = True

    def place_forget(self):
        self.placed = False

    def winfo_x(self):
        return 0

    def winfo_y(self):
        return 0


@pytest.mark.parametrize(
    "selection,combo_visible,entry_visible",
    [
        ("Другое", False, True),
        ("Нет", True, False),
        ("мм", True, False),
    ],
)
def test_on_unit_change(selection, combo_visible, entry_visible):
    combo = ComboStub(selection)
    entry = EntryStub()
    on_unit_change(combo, entry)
    assert combo.placed is combo_visible
    assert entry.placed is entry_visible

