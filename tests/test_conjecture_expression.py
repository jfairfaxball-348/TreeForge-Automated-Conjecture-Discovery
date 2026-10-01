from fractions import Fraction

import pytest

from treeforge.conjecturing.expression import evaluate_expression, evaluate_relation, is_tight


def test_exact_expression_evaluation():
    values = {"x": 6, "y": 4}
    assert evaluate_expression("((1/2 * x) + y)", values) == Fraction(7, 1)
    assert evaluate_relation("x", ">=", "(3/2 * y)", values)
    assert is_tight("x", "(3/2 * y)", values)


def test_expression_evaluator_rejects_calls_and_unknown_symbols():
    with pytest.raises(ValueError):
        evaluate_expression("__import__('os').system('echo bad')", {"x": 1})
    with pytest.raises(ValueError):
        evaluate_expression("x + z", {"x": 1})
