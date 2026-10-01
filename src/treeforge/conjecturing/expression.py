"""Exact evaluation of the restricted symbolic expressions emitted by TxGraffiti."""

from __future__ import annotations

import ast
import operator
from fractions import Fraction
from typing import Mapping

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def evaluate_expression(expression: str, values: Mapping[str, int | Fraction]) -> Fraction:
    """Evaluate a TxGraffiti arithmetic expression with exact rational arithmetic."""

    def visit(node: ast.AST) -> Fraction:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Name):
            if node.id not in values:
                raise ValueError(f"unknown symbol in conjecture expression: {node.id}")
            return Fraction(values[node.id])
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return Fraction(str(node.value))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARYOPS:
            return _UNARYOPS[type(node.op)](visit(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
            left = visit(node.left)
            right = visit(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ZeroDivisionError("zero denominator in conjecture expression")
            return _BINOPS[type(node.op)](left, right)
        raise ValueError(f"unsupported conjecture expression node: {type(node).__name__}")

    return visit(ast.parse(expression, mode="eval"))


def evaluate_relation(
    lhs: str,
    operator_symbol: str,
    rhs: str,
    values: Mapping[str, int | Fraction],
) -> bool:
    left = evaluate_expression(lhs, values)
    right = evaluate_expression(rhs, values)
    operations = {
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge,
        "==": operator.eq,
        "!=": operator.ne,
    }
    if operator_symbol not in operations:
        raise ValueError(f"unsupported relation operator: {operator_symbol}")
    return bool(operations[operator_symbol](left, right))


def is_tight(lhs: str, rhs: str, values: Mapping[str, int | Fraction]) -> bool:
    return evaluate_expression(lhs, values) == evaluate_expression(rhs, values)
