import tkinter as tk
import pytest

from widgets import select_path
import widgets.dialogs as dialogs


def test_select_path_appends_cfile_extension(monkeypatch):
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter requires a display")
    root.withdraw()
    entry = tk.Entry(root)

    monkeypatch.setattr(
        dialogs.filedialog, "asksaveasfilename", lambda **_: "/tmp/test"
    )

    select_path(entry, "save_file", extension=".cfile")
    assert entry.get() == "/tmp/test.cfile"

    root.destroy()

