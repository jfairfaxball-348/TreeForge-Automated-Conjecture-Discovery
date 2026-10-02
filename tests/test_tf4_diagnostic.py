from fractions import Fraction

from experiments.tf4_diagnostic import (
    _max_denominator,
    _ratio_coefficient,
    _rhs_features,
)


def test_tf4_diagnostic_parses_ratio_features_and_coefficients():
    assert _rhs_features("(3/13 * maximal_independent_set_count)") == (
        "maximal_independent_set_count",
    )
    assert _rhs_features("((1/3 * support_vertex_count) + (1/3 * matching_number))") == (
        "support_vertex_count",
        "matching_number",
    )
    assert _ratio_coefficient("(3/5 * matching_number)", "matching_number") == Fraction(3, 5)
    assert _ratio_coefficient("(2 * leaf_count)", "leaf_count") == 2


def test_tf4_diagnostic_denominator_summary_is_exact():
    assert _max_denominator("((1/3 * order) + (7/61 * diameter))") == 61
    assert _max_denominator("(2 * leaf_count)") == 1
