from tabs import tab4


def test_adjust_curves_root_regular_dir(tmp_path):
    resolved, err = tab4._adjust_curves_root(tmp_path)
    assert resolved is None
    assert err == f"В директории {tmp_path} отсутствует подкаталог 'curves'"


def test_adjust_curves_root_dir_with_curves_subdir(tmp_path):
    (tmp_path / "a").mkdir()
    curves = tmp_path / "curves"
    curves.mkdir()
    (tmp_path / "b").mkdir()
    resolved, err = tab4._adjust_curves_root(tmp_path)
    assert err is None
    assert resolved == curves


def test_adjust_curves_root_nonexistent_curves_dir(tmp_path):
    path = tmp_path / "curves"
    resolved, err = tab4._adjust_curves_root(path)
    assert resolved is None
    assert err


def test_adjust_curves_root_missing_curves_subdir(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    resolved, err = tab4._adjust_curves_root(project)
    assert resolved is None
    assert err == f"В директории {project} отсутствует подкаталог 'curves'"
