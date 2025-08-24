"""Evaluate mathematical expressions over arrays safely.

This module provides :func:`safe_eval_expr` which parses a mathematical
expression limited to a small subset of Python's syntax and evaluates it
against NumPy arrays. Only a predefined list of functions, constants and
operators is available to the expression. Any attempt to use other
constructs results in a :class:`ValueError` with an informative message.
"""

from __future__ import annotations

import ast
from typing import Any, Dict

import numpy as np

# Mapping of allowed function names to NumPy implementations
SAFE_FUNCTIONS: Dict[str, Any] = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "asin": np.arcsin,
    "acos": np.arccos,
    "atan": np.arctan,
    "sinh": np.sinh,
    "cosh": np.cosh,
    "tanh": np.tanh,
    "exp": np.exp,
    "log": np.log,
    "log10": np.log10,
    "sqrt": np.sqrt,
    "abs": np.abs,
    "floor": np.floor,
    "ceil": np.ceil,
    "round": np.round,
    "arctan2": np.arctan2,
    "minimum": np.minimum,
    "maximum": np.maximum,
}

# Allowed constants
SAFE_CONSTANTS: Dict[str, float] = {"pi": float(np.pi), "e": float(np.e)}

# Names that may be provided by the caller as variables
SAFE_VARS = {"x", "y"}


class SafeEvalVisitor(ast.NodeVisitor):
    """AST visitor ensuring only whitelisted nodes are present."""

    _allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Constant,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.UAdd,
        ast.USub,
    )

    def generic_visit(self, node: ast.AST) -> None:  # pragma: no cover - trivial
        if not isinstance(node, self._allowed_nodes):
            raise ValueError(f"Недопустимый элемент AST: {ast.dump(node)}")
        super().generic_visit(node)


def _eval(node: ast.AST, namespace: Dict[str, Any]) -> Any:
    """Recursively evaluate an AST node."""

    if isinstance(node, ast.Expression):
        return _eval(node.body, namespace)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return np.asarray(node.value)
        raise ValueError("Допустимы только числовые литералы")
    if isinstance(node, ast.Name):
        name = node.id
        if name in namespace:
            return namespace[name]
        raise NameError(f"Недопустимое имя: {name}")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left, namespace)
        right = _eval(node.right, namespace)
        op = node.op
        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            return left / right
        if isinstance(op, ast.Mod):
            return left % right
        if isinstance(op, ast.Pow):
            return left ** right
        raise ValueError("Недопустимая бинарная операция")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand, namespace)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand
        raise ValueError("Недопустимая унарная операция")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Вызов функции должен быть по имени")
        func_name = node.func.id
        if func_name not in SAFE_FUNCTIONS:
            raise NameError(f"Недопустимая функция: {func_name}")
        if node.keywords:
            raise ValueError("Ключевые аргументы не поддерживаются")
        func = SAFE_FUNCTIONS[func_name]
        args = [_eval(arg, namespace) for arg in node.args]
        return func(*args)
    raise ValueError(f"Недопустимый элемент выражения: {ast.dump(node)}")


def safe_eval_expr(expr: str, **vars: Any) -> np.ndarray:
    """Safely evaluate ``expr`` for NumPy arrays.

    Parameters
    ----------
    expr:
        Mathematical expression using functions from :data:`SAFE_FUNCTIONS`,
        constants ``pi`` and ``e`` and a single variable ``x`` or ``y``.
    **vars:
        Mapping providing the variable array under key ``x`` or ``y``.

    Returns
    -------
    numpy.ndarray
        Result of the expression evaluated element-wise.

    Raises
    ------
    ValueError
        If the expression contains prohibited syntax or semantic elements.
    NameError
        If the expression references unknown names or functions.
    """

    if not vars or any(name not in SAFE_VARS for name in vars):
        raise ValueError("Переданы недопустимые переменные")

    namespace: Dict[str, Any] = {**SAFE_FUNCTIONS, **SAFE_CONSTANTS, **vars}

    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:  # pragma: no cover - simple wrapper
        raise ValueError(f"Синтаксическая ошибка: {exc.msg}") from exc

    SafeEvalVisitor().visit(tree)
    result = _eval(tree, namespace)
    return np.asarray(result)


__all__ = ["safe_eval_expr"]
