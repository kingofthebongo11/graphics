from curves_scan import scan_curves


def test_scan_curves_collects_files(tmp_path):
    pilon_analysis_dir = tmp_path / "pilon-element-beam" / "static"
    pilon_analysis_dir.mkdir(parents=True)
    (pilon_analysis_dir / "file.png").touch()
    (pilon_analysis_dir / "file.txt").touch()

    uzli_analysis_dir = tmp_path / "uzli-node" / "dynamic"
    uzli_analysis_dir.mkdir(parents=True)
    (uzli_analysis_dir / "file.png").touch()
    (uzli_analysis_dir / "file.txt").touch()

    expected = {
        "pilon-element-beam": {
            "static": [
                str(pilon_analysis_dir / "file.png"),
                str(pilon_analysis_dir / "file.txt"),
            ],
        },
        "uzli-node": {
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
    (tmp_path / "pilon-element-beam" / "static").mkdir(parents=True)
    # Топ-папка без подпапок анализа
    (tmp_path / "uzli-node").mkdir()

    result, errors = scan_curves(tmp_path)

    assert result == {}
    assert sorted(errors) == sorted(
        [
            "Топ-папка 'pilon-element-beam' не содержит подпапок анализов",
            "Топ-папка 'uzli-node' не содержит подпапок анализов",
        ]
    )


def test_scan_curves_no_top_folders(tmp_path):
    result, errors = scan_curves(tmp_path)

    assert result == {}
    assert errors == ["Не найдено ни одной топ-папки"]
