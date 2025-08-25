from tabs.function4tabs4.tree_io import save_tree, load_tree
from tabs.function4tabs4.tree_schema import Tree, AnalysisFolder, CurveNode


def test_save_and_load_tree(tmp_path):
    tree = Tree(
        top="TOP",
        analyses=[AnalysisFolder(name="A", curves=[CurveNode(name="c", path="p")])],
    )
    path = tmp_path / "tree.json"
    save_tree(tree, path)
    assert path.exists()
    loaded = load_tree(path)
    assert loaded.to_dict() == tree.to_dict()
