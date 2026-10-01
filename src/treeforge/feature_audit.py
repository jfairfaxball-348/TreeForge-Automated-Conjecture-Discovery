"""Practical anti-numerology checks for finite invariant tables."""

from __future__ import annotations

from fractions import Fraction


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def audit_columns(rows: list[dict[str, object]], columns: list[str]) -> dict[str, object]:
    constants = []
    duplicates = []
    affine = []
    for column in columns:
        values = [row[column] for row in rows]
        if len(set(values)) == 1:
            constants.append({"column": column, "value": values[0]})

    for i, left in enumerate(columns):
        left_values = [row[left] for row in rows]
        for right in columns[i + 1 :]:
            right_values = [row[right] for row in rows]
            if left_values == right_values:
                duplicates.append({"left": left, "right": right})
                continue
            distinct_left = []
            for x, y in zip(left_values, right_values, strict=True):
                if all(x != old_x for old_x, _ in distinct_left):
                    distinct_left.append((x, y))
            if len(distinct_left) < 3:
                continue
            x1, y1 = distinct_left[0]
            x2, y2 = distinct_left[1]
            if x1 == x2:
                continue
            slope = Fraction(y2 - y1, x2 - x1)
            intercept = Fraction(y1) - slope * x1
            if all(Fraction(y) == slope * x + intercept for x, y in zip(left_values, right_values, strict=True)):
                affine.append(
                    {
                        "left": left,
                        "right": right,
                        "right_equals": f"{_fraction_text(slope)}*{left}+{_fraction_text(intercept)}",
                    }
                )
    return {"constants": constants, "duplicates": duplicates, "affine_equivalences": affine}


def known_identity_violations(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    violations = []
    for row in rows:
        code = row.get("tree_code")
        if {"order", "edge_count"} <= row.keys() and row["edge_count"] != row["order"] - 1:
            violations.append({"tree_code": code, "identity": "edge_count = order - 1"})
        if {"degree_sum", "edge_count"} <= row.keys() and row["degree_sum"] != 2 * row["edge_count"]:
            violations.append({"tree_code": code, "identity": "degree_sum = 2 edge_count"})
        if {"independence_number", "matching_number", "order"} <= row.keys():
            if row["independence_number"] + row["matching_number"] != row["order"]:
                violations.append({"tree_code": code, "identity": "independence_number + matching_number = order"})
    return violations
