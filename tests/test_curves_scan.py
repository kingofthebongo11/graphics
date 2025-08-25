from curves_scan import scan_curves


def test_scan_curves_collects_files(tmp_path):
    pilon_analysis_dir = tmp_path / "01-pilon-element-beam" / "10-static"
    pilon_analysis_dir.mkdir(parents=True)
    (pilon_analysis_dir / "file.png").touch()
    (pilon_analysis_dir / "file.txt").touch()

    uzli_analysis_dir = tmp_path / "2-uzli-node" / "3-dynamic"
    uzli_analysis_dir.mkdir(parents=True)
    (uzli_analysis_dir / "file.png").touch()
    (uzli_analysis_dir / "file.txt").touch()

    expected = {
        "01-pilon-element-beam": {
            "static": [
                str(pilon_analysis_dir / "file.png"),
                str(pilon_analysis_dir / "file.txt"),
            ],
        },
        "2-uzli-node": {
            "dynamic": [
                str(uzli_analysis_dir / "file.png"),
                str(uzli_analysis_dir / "file.txt"),
            ],
        },
    }

    result, errors = scan_curves(tmp_path)

    for analyses in expected.values():
        for files in analyses.values():
            files.sort()
    for analyses in result.values():
        for files in analyses.values():
            files.sort()

    assert result == expected
    assert not errors


def test_scan_curves_empty_or_missing(tmp_path):
    # Топ-папка с пустой подпапкой анализа
    (tmp_path / "1-pilon-element-beam" / "2-static").mkdir(parents=True)
    # Топ-папка без подпапок анализа
    (tmp_path / "02-uzli-node").mkdir()

    result, errors = scan_curves(tmp_path)

    assert result == {}
    assert sorted(errors) == sorted(
        [
            "Подпапка анализа 'static' в топ-папке '1-pilon-element-beam' не содержит файлов",
            "Топ-папка '02-uzli-node' не содержит подпапок анализов",
        ]
    )


def test_scan_curves_duplicate_base_names(tmp_path):
    first = tmp_path / "01-beam" / "10-static"
    first.mkdir(parents=True)
    (first / "f1.png").touch()

    second = tmp_path / "02-beam" / "10-static"
    second.mkdir(parents=True)
    (second / "f2.png").touch()

    expected = {
        "01-beam": {"static": [str(first / "f1.png")]},
        "02-beam": {"static": [str(second / "f2.png")]},
    }

    result, errors = scan_curves(tmp_path)

    assert result == expected
    assert not errors


def test_scan_curves_no_top_folders(tmp_path):
    result, errors = scan_curves(tmp_path)

    assert result == {}
    assert errors == ["Не найдено ни одной топ-папки"]
