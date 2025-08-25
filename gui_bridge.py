"""Конвертация дерева GUI в модель данных."""
from __future__ import annotations

from naming import safe_name
from tree_schema import EntityNode, AnalysisNode, FileNode
from validators import (
    ensure_unique_names,
    validate_analysis_type,
    validate_entity,
    validate_filename,
)


class _TreeItemProtocol:
    """Простой протокол для элементов дерева.

    Он описывает минимальные методы :class:`QTreeWidgetItem`, которые
    используются функцией :func:`tree_from_gui`. Предполагается, что
    передаваемый ``tree_widget`` поддерживает методы ``topLevelItem`` и
    ``topLevelItemCount``, возвращающие объекты, реализующие этот протокол.
    """

    def text(self, column: int) -> str:  # pragma: no cover - протокол
        raise NotImplementedError

    def childCount(self) -> int:  # pragma: no cover - протокол
        raise NotImplementedError

    def child(self, index: int) -> "_TreeItemProtocol":  # pragma: no cover
        raise NotImplementedError


class _TreeWidgetProtocol:
    """Протокол для виджетов дерева GUI."""

    def topLevelItemCount(self) -> int:  # pragma: no cover - протокол
        raise NotImplementedError

    def topLevelItem(self, index: int) -> _TreeItemProtocol:  # pragma: no cover
        raise NotImplementedError


def _get_child(item: _TreeItemProtocol, index: int) -> _TreeItemProtocol:
    try:
        return item.child(index)
    except Exception as exc:  # pragma: no cover - защитный код
        raise ValueError("Неверная структура дерева GUI") from exc


def tree_from_gui(tree_widget: _TreeWidgetProtocol) -> EntityNode:
    """Строит модель :class:`EntityNode` из дерева GUI.

    Ожидается следующая структура дерева::

        user_name
          └─ entity_kind
               ├─ element_type (для ``entity_kind == 'element'``)
               └─ analysis_type
                    └─ id

    На каждом уровне выполняются проверки при помощи модуля
    :mod:`validators`, а все строки проходят через :func:`naming.safe_name`.
    """

    if tree_widget.topLevelItemCount() != 1:
        raise ValueError("Ожидается ровно один верхний узел")

    user_item = tree_widget.topLevelItem(0)
    user_name = safe_name(user_item.text(0).strip())

    if user_item.childCount() == 0:
        raise ValueError("Отсутствует узел entity_kind")

    entity_item = _get_child(user_item, 0)
    entity_kind = safe_name(entity_item.text(0).strip())

    element_type: str | None = None
    analysis_parent = entity_item
    if entity_kind == "element":
        if entity_item.childCount() == 0:
            raise ValueError("Отсутствует узел element_type")
        element_item = _get_child(entity_item, 0)
        element_type = safe_name(element_item.text(0).strip())
        analysis_parent = element_item

    root = EntityNode(
        user_name=user_name,
        entity_kind=entity_kind,  # type: ignore[arg-type]
        element_type=element_type,  # type: ignore[arg-type]
    )
    validate_entity(root.to_dict())

    for i in range(analysis_parent.childCount()):
        analysis_item = _get_child(analysis_parent, i)
        analysis_type = safe_name(analysis_item.text(0).strip())
        validate_analysis_type(analysis_type)
        analysis_node = AnalysisNode(analysis_type=analysis_type)

        for j in range(analysis_item.childCount()):
            file_item = _get_child(analysis_item, j)
            id_str = safe_name(file_item.text(0).strip())
            validate_filename(id_str)
            file_node = FileNode(id=int(id_str))
            analysis_node.children.append(file_node)

        ensure_unique_names(analysis_node.children, key="id")
        root.children.append(analysis_node)

    ensure_unique_names(root.children, key="analysis_type")
    return root

__all__ = ["tree_from_gui"]
