from treeforge.feature_audit import audit_columns, known_identity_violations


def test_feature_audit_detects_constant_duplicate_and_affine_columns():
    rows = [
        {"a": 1, "b": 3, "c": 3, "k": 7},
        {"a": 2, "b": 5, "c": 5, "k": 7},
        {"a": 3, "b": 7, "c": 7, "k": 7},
    ]
    result = audit_columns(rows, ["a", "b", "c", "k"])
    assert {"column": "k", "value": 7} in result["constants"]
    assert {"left": "b", "right": "c"} in result["duplicates"]
    assert any(item["left"] == "a" and item["right"] == "b" for item in result["affine_equivalences"])


def test_known_tree_identity_checks():
    rows = [
        {
            "tree_code": "x",
            "order": 5,
            "edge_count": 4,
            "degree_sum": 8,
            "matching_number": 2,
            "independence_number": 3,
        }
    ]
    assert known_identity_violations(rows) == []
