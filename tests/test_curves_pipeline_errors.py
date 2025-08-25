import logging
from curves_pipeline import build_curves_report


def test_build_curves_report_propagates_scan_errors(tmp_path, caplog):
    caplog.set_level(logging.WARNING)
    _, errors = build_curves_report(tmp_path)
    log_file = tmp_path / "errors.log"

    assert log_file.exists()
    assert "Не найдено ни одной топ-папки" in log_file.read_text(encoding="utf-8")
    assert any("Не найдено ни одной топ-папки" in e for e in errors)
    assert "обнаружены проблемы" in caplog.text.lower()
