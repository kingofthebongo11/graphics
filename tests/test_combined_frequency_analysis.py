import tempfile

from tabs.functions_for_tab1.curves_from_file.combined_curve import read_X_Y_from_combined


def _create_temp_file(content: str):
    tmp = tempfile.NamedTemporaryFile('w+', delete=False)
    tmp.write(content)
    tmp.flush()
    return tmp


def test_read_combined_frequency_analysis():
    tmp = _create_temp_file(
        "t XN Xeig Xmass prXmass totalprXmass\n"
        "[0.0, 1, 10.0, 100.0, '50%', '100%']\n"
        "[1.0, 2, 12.0, 110.0, '60%', '110%']\n"
    )
    curve_info = {
        'X_source': {
            'source': 'Частотный анализ',
            'curve_file': tmp.name,
            'parameter': 'Время',
            'direction': 'X',
        },
        'Y_source': {
            'source': 'Частотный анализ',
            'curve_file': tmp.name,
            'parameter': 'Частота',
            'direction': 'X',
        },
    }
    read_X_Y_from_combined(curve_info)
    assert curve_info['X_values'] == [0.0, 1.0]
    assert curve_info['Y_values'] == [10.0, 12.0]

