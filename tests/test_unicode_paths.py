import os
from tabs.function4tabs4.cfile_writer import write_cfile
from tabs.function4tabs4.tree_io import save_tree, load_tree
from tabs.function4tabs4.tree_schema import Tree, AnalysisFolder, CurveNode


def test_cyrillic_paths(tmp_path):
    workdir = tmp_path / "папка"
    workdir.mkdir()

    cfile_path = workdir / "команды.cfile"
    tree_path = workdir / "дерево.json"

    # Проверка записи и чтения .cfile по байтовому пути
    commands = ["привет", "мир"]
    write_cfile(commands, os.fsencode(cfile_path))
    assert cfile_path.read_text(encoding="utf-8") == "привет\nмир\n"

    # Проверка сохранения и загрузки дерева по байтовому пути
    tree = Tree(top="T", analyses=[AnalysisFolder(name="A", curves=[CurveNode(name="c", path="p")])])
    save_tree(tree, os.fsencode(tree_path))
    loaded = load_tree(os.fsencode(tree_path))
    assert loaded.to_dict() == tree.to_dict()
