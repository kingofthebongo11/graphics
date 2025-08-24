from pathlib import Path

from tabs.function4tabs4.cfile_writer import write_cfile
from tabs.function4tabs4.tree_io import save_tree, load_tree
from tabs.function4tabs4.tree_schema import AnalysisFolder, CurveNode, Tree


def test_relative_and_mixed_paths(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("sub").mkdir()

    rel_path = Path("sub") / "commands.cfile"
    result = write_cfile(["a"], rel_path)
    assert result == rel_path.resolve()
    assert rel_path.read_text(encoding="utf-8") == "a\n"

    tree = Tree(top="T", analyses=[AnalysisFolder(name="A", curves=[CurveNode(name="c", path="p")])])
    mixed_path = Path("sub") / ".." / "sub" / "tree.json"
    save_tree(tree, mixed_path)
    loaded = load_tree(mixed_path)
    assert loaded.to_dict() == tree.to_dict()
