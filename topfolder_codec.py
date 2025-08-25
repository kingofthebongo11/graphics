"""Utilities for encoding and decoding top-level folder names."""

from __future__ import annotations

from typing import Optional, Tuple

# Allowed kinds of entities and element types.
ENTITY_KINDS = {"element", "node"}
ELEMENT_TYPES = {"beam", "shell", "solid", "spring", "mass", "rigid"}

# Characters that must not appear in user name.
FORBIDDEN_IN_USER = set("-/\\")


def _validate_user_name(user_name: str) -> str:
    """Validate the user name ensuring it is non-empty and has no forbidden symbols."""
    if not user_name:
        raise ValueError("Имя пользователя не может быть пустым.")
    if any(ch in FORBIDDEN_IN_USER for ch in user_name):
        raise ValueError("Имя пользователя содержит запрещённые символы.")
    return user_name


def encode_topfolder(user_name: str, entity_kind: str, element_type: Optional[str] = None) -> str:
    """Encode components into a folder name.

    Parameters
    ----------
    user_name: str
        Имя пользователя. Не может быть пустым или содержать запрещённые символы.
    entity_kind: str
        Тип сущности. Допустимые значения см. в ENTITY_KINDS.
    element_type: Optional[str]
        Тип элемента. Требуется, если entity_kind равно ``"element"``.
    """

    _validate_user_name(user_name)
    if entity_kind not in ENTITY_KINDS:
        raise ValueError("Недопустимый тип сущности.")

    if entity_kind == "element":
        if element_type is None:
            raise ValueError("Для 'element' необходимо указать тип элемента.")
        if element_type not in ELEMENT_TYPES:
            raise ValueError("Недопустимый тип элемента.")
        return f"{user_name}-{entity_kind}-{element_type}"

    if element_type is not None:
        raise ValueError("Тип элемента можно указывать только для 'element'.")
    return f"{user_name}-{entity_kind}"


def decode_topfolder(folder_name: str) -> Tuple[str, str, Optional[str]]:
    """Decode folder name into components.

    Допускается ведущий префикс вида ``"<число>-"``. Он игнорируется при
    декодировании и используется только для уточнения сообщений об ошибках.

    Returns
    -------
    tuple
        ``(user_name, entity_kind, element_type)`` где ``element_type`` может
        быть ``None``.
    """

    prefix = None
    if "-" in folder_name:
        first, rest = folder_name.split("-", 1)
        if first.isdigit():
            prefix = first
            folder_name = rest
            if not folder_name:
                raise ValueError("Неверный формат имени папки с префиксом.")

    parts = folder_name.split("-")
    if len(parts) not in (2, 3):
        msg = "Неверный формат имени папки с префиксом." if prefix else "Неверный формат имени папки."
        raise ValueError(msg)

    user_name = _validate_user_name(parts[0])
    entity_kind = parts[1]
    element_type: Optional[str] = None

    if entity_kind not in ENTITY_KINDS:
        raise ValueError("Недопустимый тип сущности.")

    if entity_kind == "element":
        if len(parts) != 3:
            raise ValueError("Для 'element' требуется тип элемента.")
        element_type = parts[2]
        if element_type not in ELEMENT_TYPES:
            raise ValueError("Недопустимый тип элемента.")
    else:
        if len(parts) != 2:
            raise ValueError("Тип элемента можно указывать только для 'element'.")

    return user_name, entity_kind, element_type
