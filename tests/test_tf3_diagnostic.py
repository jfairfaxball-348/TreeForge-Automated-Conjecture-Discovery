from experiments.tf3_diagnostic import _max_denominator, _rhs_support


def test_tf3_complexity_parser_counts_feature_support_and_denominators():
    rhs = "(((1/8 * order) + -5/4) + support_vertex_count)"
    assert _rhs_support(rhs) == 2
    assert _max_denominator(rhs) == 8
