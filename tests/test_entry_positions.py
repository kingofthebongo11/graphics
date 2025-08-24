import ui.constants as ui_const
from tabs.tab1 import on_combo_changeX_Y_labels, on_unit_change


class ComboStub:
    def __init__(self, selection):
        self._selection = selection

    def get(self):
        return self._selection

    def winfo_x(self):
        return ui_const.AXIS_COMBO_X

    def winfo_y(self):
        return 0


class EntryRecorder:
    def __init__(self):
        self.coords = {}
        self.mapped = False

    def place(self, **kwargs):
        self.coords = kwargs
        self.mapped = True

    def place_forget(self):
        self.mapped = False

    def winfo_ismapped(self):
        return self.mapped

    def config(self, **kwargs):
        pass


class LabelStub:
    def place(self, *args, **kwargs):
        pass

    def place_forget(self):
        pass


class SizeComboStub:
    def __init__(self):
        self.values = []
        self.placed = False

    def __setitem__(self, key, value):
        if key == "values":
            self.values = value

    def set(self, value):
        pass

    def place(self, **kwargs):
        self.placed = True

    def place_forget(self):
        self.placed = False

    def current(self, index):
        pass

    def winfo_y(self):
        return 0


class UnitComboStub:
    def __init__(self, selection="Другое"):
        self._selection = selection
        self.placed = True

    def get(self):
        return self._selection

    def place_forget(self):
        self.placed = False

    def winfo_y(self):
        return 0


def test_axis_custom_entry_position():
    combo = ComboStub("Другое")
    entry = EntryRecorder()
    label = LabelStub()
    size_combo = SizeComboStub()
    size_entry = EntryRecorder()
    on_combo_changeX_Y_labels(combo, entry, label, size_combo, size_entry)
    assert entry.coords["x"] == ui_const.AXIS_ENTRY_X
    assert entry.coords["y"] == combo.winfo_y()


def test_custom_unit_entry_position():
    combo = UnitComboStub()
    entry = EntryRecorder()
    on_unit_change(combo, entry)
    assert entry.coords["x"] == ui_const.AXIS_UNIT_X
    assert entry.coords["y"] == combo.winfo_y()

