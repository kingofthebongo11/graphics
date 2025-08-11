import matplotlib
matplotlib.use('Agg')
from types import SimpleNamespace
from unittest.mock import patch

from tabs.functions_for_tab1 import plotting


def test_save_file_warns_without_graph():
    entry = SimpleNamespace(get=lambda: 'graph')
    fmt_widget = SimpleNamespace(get=lambda: 'png')
    graph_info = {}
    with patch('tabs.functions_for_tab1.plotting.filedialog.asksaveasfilename') as ask, \
         patch('tabs.functions_for_tab1.plotting.messagebox.showwarning') as warn:
        plotting.save_file(entry, fmt_widget, graph_info)
        warn.assert_called_once_with("Предупреждение", "Сначала постройте график")
        ask.assert_not_called()
