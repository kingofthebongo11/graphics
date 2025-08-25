from curves_pipeline import build_curves_report


def test_build_curves_report_propagates_scan_errors(tmp_path):
    _, errors = build_curves_report(tmp_path)
    assert any("Не найдено ни одной топ-папки" in e for e in errors)
