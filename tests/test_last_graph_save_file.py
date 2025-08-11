import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure

from types import SimpleNamespace
from unittest.mock import patch

from tabs.functions_for_tab1 import plotting
from tabs import tab1


def test_save_file_uses_updated_last_graph(tmp_path):
    # убеждаемся, что last_graph используется как общий объект
    assert tab1.last_graph is plotting.last_graph

    # имитируем обновление графика
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot([0, 1], [0, 1])
    plotting.last_graph.clear()
    plotting.last_graph.update({
        'curves_info': [{'X_values': [0, 1], 'Y_values': [0, 1]}],
        'X_label': 'X',
        'Y_label': 'Y',
        'title': 'T',
        'fig': fig,
    })

    entry = SimpleNamespace(get=lambda: 'graph')
    file_path = tmp_path / 'out.png'

    with patch('tabs.functions_for_tab1.plotting.filedialog.asksaveasfilename', return_value=str(file_path)), \
         patch('tabs.functions_for_tab1.plotting.messagebox.showinfo'), \
         patch('tabs.functions_for_tab1.plotting.messagebox.showerror'):
        tab1.save_file(entry, tab1.last_graph)

    assert file_path.exists()
