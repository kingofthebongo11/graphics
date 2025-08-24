import pytest

from gui_bridge import tree_from_gui
from tree_schema import EntityNode, AnalysisNode, FileNode
from validators import ValidationError


class FakeItem:
    def __init__(self, text, children=None):
        self._text = text
        self._children = children or []

    def text(self, column):
        return self._text

    def childCount(self):
        return len(self._children)

    def child(self, index):
        return self._children[index]


class FakeTreeWidget:
    def __init__(self, items):
        self._items = items

    def topLevelItemCount(self):
        return len(self._items)

    def topLevelItem(self, index):
        return self._items[index]


def test_tree_from_gui_basic():
    tree = FakeTreeWidget([
        FakeItem("User?Name", [
            FakeItem("element", [
                FakeItem("beam", [
                    FakeItem("static", [FakeItem("1"), FakeItem("2")]),
                    FakeItem("dynamic", [FakeItem("3")]),
                ])
            ])
        ])
    ])

    root = tree_from_gui(tree)
    assert root == EntityNode(
        user_name="UserName",
        entity_kind="element",
        element_type="beam",
        children=[
            AnalysisNode(
                analysis_type="static",
                children=[FileNode(id=1), FileNode(id=2)],
            ),
            AnalysisNode(
                analysis_type="dynamic",
                children=[FileNode(id=3)],
            ),
        ],
    )


def test_tree_from_gui_duplicate_ids():
    tree = FakeTreeWidget([
        FakeItem("user", [
            FakeItem("node", [
                FakeItem("static", [FakeItem("1"), FakeItem("1")])
            ])
        ])
    ])
    with pytest.raises(ValidationError):
        tree_from_gui(tree)


def test_tree_from_gui_invalid_analysis():
    tree = FakeTreeWidget([
        FakeItem("user", [
            FakeItem("node", [
                FakeItem("unknown", [FakeItem("1")])
            ])
        ])
    ])
    with pytest.raises(ValidationError):
        tree_from_gui(tree)
