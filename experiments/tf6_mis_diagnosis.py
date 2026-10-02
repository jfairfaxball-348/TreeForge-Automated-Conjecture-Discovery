#!/usr/bin/env python3
"""Reproduce the TF6 exposed-data diagnosis of maximal_independent_set_count."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

import networkx as nx

from experiments.tf5_analysis import MIS_IDS, RELATIONS, domination_number_dp
from treeforge.invariants.core import (
    matching_number,
    maximal_independent_set_count,
    support_vertex_count,
)
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import canonical_tree_code, generate_unlabeled_trees

STARTING_MAIN = "1a0bd2363908659a76ebba8a9d0cc1662f4b4980"
OUTPUT = Path("experiments/TF6-DIAG-0001/diagnosis.json")
CANDIDATE_BATCH = Path("experiments/TF4-0001/candidate_batch.json")
CANDIDATE_REGISTRY = Path("data/registry/candidates.jsonl")
EXPERIMENT_REGISTRY = Path("data/registry/experiments.jsonl")


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _values(graph: nx.Graph) -> dict[str, int | str]:
    return {
        "order": graph.number_of_nodes(),
        "tree_code": canonical_tree_code(graph),
        "diameter": nx.diameter(graph),
        "support_vertex_count": support_vertex_count(graph),
        "matching_number": matching_number(graph),
        "maximal_independent_set_count": maximal_independent_set_count(graph),
        "domination_number": domination_number_dp(graph),
    }


def _relation_bound(
    row: dict[str, int | str],
    relation: tuple[str, dict[str, Fraction], Fraction],
) -> Fraction:
    _, coefficients, constant = relation
    return constant + sum(coefficient * int(row[name]) for name, coefficient in coefficients.items())


def _relation_slack(
    row: dict[str, int | str],
    relation: tuple[str, dict[str, Fraction], Fraction],
) -> Fraction:
    operator, _, _ = relation
    bound = _relation_bound(row, relation)
    gamma = Fraction(int(row["domination_number"]))
    return bound - gamma if operator == "<=" else gamma - bound


def _candidate_metadata() -> dict[str, dict[str, object]]:
    batch = json.loads(CANDIDATE_BATCH.read_text(encoding="utf-8"))
    selected = {row["candidate_id"]: row for row in batch if row["candidate_id"] in MIS_IDS}
    if sorted(selected) != sorted(MIS_IDS):
        raise AssertionError("TF4 candidate batch does not contain the exact TF6 MIS fan")

    tf6_snapshot: dict[str, dict[str, object]] = {}
    for row in _jsonl(CANDIDATE_REGISTRY):
        if row["candidate_id"] in MIS_IDS and row["revision"] == 5:
            tf6_snapshot[str(row["candidate_id"])] = row
    if sorted(tf6_snapshot) != sorted(MIS_IDS):
        raise AssertionError("TF6 revision-5 candidate snapshot changed")

    dossier: dict[str, dict[str, object]] = {}
    for candidate_id in MIS_IDS:
        original = selected[candidate_id]
        current = tf6_snapshot[candidate_id]
        operator, coefficients, constant = RELATIONS[candidate_id]
        other = [
            (name, coefficient)
            for name, coefficient in coefficients.items()
            if name != "maximal_independent_set_count"
        ]
        dossier[candidate_id] = {
            "statement": original["statement"],
            "operator": operator,
            "constant": _fraction(constant),
            "maximal_independent_set_count_coefficient": _fraction(
                coefficients["maximal_independent_set_count"]
            ),
            "other_feature": None if not other else other[0][0],
            "other_feature_coefficient": None if not other else _fraction(other[0][1]),
            "source_feature_pairs": original["discovery_evidence"]["source_feature_pairs"],
            "discovery_touch_count": original["discovery_evidence"]["structured_relation"][
                "discovery_touch_count"
            ],
            "discovery_equality_examples": original["equality_or_sharp_examples"],
            "order14_holdout_status": current["holdout_status"],
            "tf4_hostile_status": current["adversarial_status"],
            "current_lifecycle_state": current["lifecycle_state"],
            "current_revision": current["revision"],
        }
        if current["lifecycle_state"] != "ADVERSARIAL_PASSED":
            raise AssertionError(f"unexpected TF6 starting state for {candidate_id}")
        if current["holdout_status"]["status"] != "PASSED":
            raise AssertionError(f"order-14 holdout is not passed for {candidate_id}")
        if current["adversarial_status"]["status"] != "PASSED":
            raise AssertionError(f"TF4 hostile set is not passed for {candidate_id}")
    return dossier


def _stability(
    rows: list[dict[str, int | str]],
    dossier: dict[str, dict[str, object]],
) -> None:
    windows = {
        "discovery_orders_2_10": (2, 10),
        "cumulative_through_11": (2, 11),
        "cumulative_through_12": (2, 12),
        "cumulative_through_13": (2, 13),
        "cumulative_through_14": (2, 14),
    }
    for candidate_id in MIS_IDS:
        relation = RELATIONS[candidate_id]
        per_order = {}
        for order in range(11, 15):
            order_rows = [row for row in rows if row["order"] == order]
            slacks = [_relation_slack(row, relation) for row in order_rows]
            per_order[str(order)] = {
                "tree_count": len(order_rows),
                "failures": sum(value < 0 for value in slacks),
                "equalities": sum(value == 0 for value in slacks),
            }

        cumulative = {}
        for name, (lower, upper) in windows.items():
            sample = [row for row in rows if lower <= int(row["order"]) <= upper]
            slacks = [_relation_slack(row, relation) for row in sample]
            failures = sum(value < 0 for value in slacks)
            equalities = sum(value == 0 for value in slacks)
            cumulative[name] = {
                "tree_count": len(sample),
                "failures": failures,
                "equalities": equalities,
                "supporting_hyperplane_on_exposed_sample": failures == 0 and equalities > 0,
            }

        dossier[candidate_id]["exposed_order_equality_counts_11_14"] = per_order
        dossier[candidate_id]["cumulative_support_geometry"] = cumulative
        if any(item["failures"] for item in per_order.values()):
            raise AssertionError(f"exposed failure for {candidate_id}")
        if any(not item["equalities"] for item in per_order.values()):
            raise AssertionError(f"lost equality support for {candidate_id}")


def _geometry(rows: list[dict[str, int | str]]) -> dict[str, object]:
    equality_tree_sets = {}
    equality_vector_sets = {}
    for candidate_id in MIS_IDS:
        relation = RELATIONS[candidate_id]
        equality_tree_sets[candidate_id] = frozenset(
            (int(row["order"]), str(row["tree_code"]))
            for row in rows
            if _relation_slack(row, relation) == 0
        )
        equality_vector_sets[candidate_id] = frozenset(
            (
                int(row["domination_number"]),
                int(row["diameter"]),
                int(row["support_vertex_count"]),
                int(row["matching_number"]),
                int(row["maximal_independent_set_count"]),
            )
            for row in rows
            if _relation_slack(row, relation) == 0
        )

    def duplicate_groups(mapping: dict[str, frozenset[object]]) -> list[list[str]]:
        groups: defaultdict[frozenset[object], list[str]] = defaultdict(list)
        for candidate_id, values in mapping.items():
            groups[values].append(candidate_id)
        return sorted(sorted(ids) for ids in groups.values() if len(ids) > 1)

    dominance = []
    for stronger, weaker in itertools.permutations(MIS_IDS, 2):
        first = RELATIONS[stronger]
        second = RELATIONS[weaker]
        if first[0] != second[0]:
            continue
        if first[0] == "<=":
            ordered = all(_relation_bound(row, first) <= _relation_bound(row, second) for row in rows)
        else:
            ordered = all(_relation_bound(row, first) >= _relation_bound(row, second) for row in rows)
        strict = any(_relation_bound(row, first) != _relation_bound(row, second) for row in rows)
        if ordered and strict:
            dominance.append([stronger, weaker])

    vector_multiplicity = Counter(
        (
            int(row["domination_number"]),
            int(row["diameter"]),
            int(row["support_vertex_count"]),
            int(row["matching_number"]),
            int(row["maximal_independent_set_count"]),
        )
        for row in rows
    )
    common_vectors = []
    for vector, tree_count in vector_multiplicity.items():
        sample = {
            "domination_number": vector[0],
            "diameter": vector[1],
            "support_vertex_count": vector[2],
            "matching_number": vector[3],
            "maximal_independent_set_count": vector[4],
        }
        tight = [
            candidate_id
            for candidate_id in MIS_IDS
            if _relation_slack(sample, RELATIONS[candidate_id]) == 0
        ]
        if len(tight) >= 3:
            by_order = Counter(
                int(row["order"])
                for row in rows
                if (
                    int(row["domination_number"]),
                    int(row["diameter"]),
                    int(row["support_vertex_count"]),
                    int(row["matching_number"]),
                    int(row["maximal_independent_set_count"]),
                )
                == vector
            )
            common_vectors.append(
                {
                    "vector": {
                        "domination_number": vector[0],
                        "diameter": vector[1],
                        "support_vertex_count": vector[2],
                        "matching_number": vector[3],
                        "maximal_independent_set_count": vector[4],
                    },
                    "tight_candidate_count": len(tight),
                    "tight_candidate_ids": tight,
                    "tree_count_orders_1_14": tree_count,
                    "tree_counts_by_order": {str(k): by_order[k] for k in sorted(by_order)},
                }
            )
    common_vectors.sort(
        key=lambda item: (
            -int(item["tight_candidate_count"]),
            -int(item["tree_count_orders_1_14"]),
            tuple(item["vector"].values()),
        )
    )

    operator_counts = Counter(RELATIONS[candidate_id][0] for candidate_id in MIS_IDS)
    family_counts = Counter()
    for candidate_id in MIS_IDS:
        features = set(RELATIONS[candidate_id][1])
        if features == {"maximal_independent_set_count"}:
            family_counts["mis_only"] += 1
        elif "support_vertex_count" in features:
            family_counts["support_plus_mis"] += 1
        elif "diameter" in features:
            family_counts["diameter_plus_mis"] += 1
        elif "matching_number" in features:
            family_counts["matching_plus_mis"] += 1

    return {
        "coordinate_family_counts": dict(family_counts),
        "operator_counts": {"upper_bounds": operator_counts["<="], "lower_bounds": operator_counts[">="]},
        "identical_equality_tree_set_groups": duplicate_groups(equality_tree_sets),
        "identical_equality_invariant_vector_set_groups": duplicate_groups(equality_vector_sets),
        "exposed_pointwise_dominance_relations": dominance,
        "dominance_algebra": {
            "TF-001091_over_TF-001034": (
                "On any tree, TF-001091's upper RHS is at most TF-001034's exactly when "
                "MIS >= 3*support_vertex_count - 4. TF6 verifies this only on exposed data."
            ),
            "TF-001095_over_TF-001037": (
                "On any tree, TF-001095's upper RHS is at most TF-001037's exactly when "
                "MIS >= 5*support_vertex_count - 12. TF6 verifies this only on exposed data."
            ),
        },
        "largest_common_tight_vectors": common_vectors[:12],
        "facet_chain_summary": {
            "mis_only_upper": ["TF-001033", "TF-001034", "TF-001037"],
            "support_plus_mis_upper": [
                "TF-001090",
                "TF-001091",
                "TF-001093",
                "TF-001095",
                "TF-001099",
            ],
            "support_plus_mis_lower": ["TF-001098"],
            "diameter_plus_mis_upper": [
                "TF-001134",
                "TF-001135",
                "TF-001137",
                "TF-001139",
                "TF-001141",
                "TF-001142",
                "TF-001144",
                "TF-001145",
            ],
            "diameter_plus_mis_lower": ["TF-001140"],
            "matching_plus_mis_lower": ["TF-001154", "TF-001155"],
        },
        "projection_diagnosis": (
            "Two MIS-only upper facets are strictly dominated on the exposed corpus by "
            "support/MIS facets (TF-001091 over TF-001034; TF-001095 over TF-001037). "
            "TF-001033 is not. This is finite geometry, not a universal implication."
        ),
    }


def _structural_diagnosis(rows: list[dict[str, int | str]]) -> dict[str, object]:
    by_order = defaultdict(list)
    for row in rows:
        by_order[int(row["order"])].append(row)

    path_counts = [maximal_independent_set_count(nx.path_graph(order)) for order in range(1, 21)]
    for order in range(4, 21):
        if path_counts[order - 1] != path_counts[order - 3] + path_counts[order - 4]:
            raise AssertionError("path MIS recurrence changed")

    return {
        "meaning": (
            "A maximal independent set is exactly an independent dominating set, so the count "
            "has a direct domination-theoretic interpretation independent of TF4 coefficients."
        ),
        "rooted_three_state_recurrence": {
            "states": {
                "A": "root selected",
                "B": "root unselected and dominated by at least one selected child",
                "C": "root unselected and not internally dominated; requires selected parent",
            },
            "formula": {
                "A_v": "product_u (B_u + C_u)",
                "C_v": "product_u B_u",
                "B_v": "product_u (A_u + B_u) - product_u B_u",
                "MIS_T": "A_r + B_r",
            },
        },
        "local_operations": {
            "leaf_attachment": (
                "A leaf child has state (1,0,1). Adding it to a parent's existing local state "
                "(A,B,C) gives (A, B+C, 0)."
            ),
            "support_vertex_leaf_duplication": (
                "Once that parent already has a leaf child its C-state is zero, so any further "
                "twin-leaf attachment leaves (A,B,0) unchanged. Thus duplicating a leaf at an "
                "existing support vertex does not change the whole-tree MIS count."
            ),
            "fixed_branch_attachment": (
                "If a rooted attached branch has state (a,b,c), adding it to a parent's existing "
                "local state (A,B,C) gives ((b+c)A, (a+b)B+aC, bC)."
            ),
            "repeated_fixed_branches": (
                "For a root with m identical branch children (a,b,c), the whole-tree count is "
                "(b+c)^m + (a+b)^m - b^m, explicitly exhibiting multiplicative/exponential scale."
            ),
            "path_subdivision": (
                "For paths, M(P_n)=M(P_{n-2})+M(P_{n-3}) for n>=4, with 1,2,2 initially; "
                "repeated subdivision therefore has Padovan-type exponential growth."
            ),
            "corona_extension": (
                "For any tree H, maximal independent sets of H corona K1 are in bijection with "
                "all independent sets of H: choose each base vertex or, when it is not chosen, "
                "its private leaf."
            ),
            "caterpillars_and_spiders": (
                "Their repeated spine/arm pieces compose the same finite-state messages; periodic "
                "families therefore admit transfer recurrences, but no root-independent scalar "
                "state component is canonical apart from the final total A+B."
            ),
        },
        "path_counts_orders_1_20": path_counts,
        "mis_count_ranges_by_exposed_order": {
            str(order): [
                min(int(row["maximal_independent_set_count"]) for row in by_order[order]),
                max(int(row["maximal_independent_set_count"]) for row in by_order[order]),
            ]
            for order in range(1, 15)
        },
        "known_order_extremal_envelope": {
            "n_even_2k": "2^(k-1)+1",
            "n_odd_2k_plus_1": "2^k",
            "source": (
                "Wilf (1986), The Number of Maximal Independent Sets in a Tree; "
                "Sagan (1988), A Note on Independent Sets in Trees, DOI 10.1137/0401012."
            ),
            "interpretation": (
                "Exponential raw scale is intrinsic and extremally sharp, not a plotting artifact."
            ),
        },
    }


def _transformations() -> list[dict[str, str]]:
    return [
        {
            "coordinate": "raw maximal_independent_set_count",
            "independent_meaning": "exact number of independent dominating sets",
            "decision": "retain",
            "reason": (
                "It is exact, root-independent, combinatorial, and recurrence-natural. The 20 "
                "facets remain supporting through every exposed extension to order 14."
            ),
        },
        {
            "coordinate": "log(maximal_independent_set_count)",
            "independent_meaning": "logarithmic enumerative scale",
            "decision": "reject_for_now",
            "reason": (
                "The recurrence is sum-product rather than multiplicative, so log does not linearize "
                "tree composition generally; it also replaces exact rational hull coordinates by "
                "non-exact real values without an independent gamma-versus-log theorem."
            ),
        },
        {
            "coordinate": "log(maximal_independent_set_count) / order",
            "independent_meaning": "per-vertex exponential growth rate",
            "decision": "reject_for_now",
            "reason": (
                "Meaningful for asymptotic families but not canonical for individual finite-tree "
                "linear inequalities; it entangles MIS with order and loses absolute count scale."
            ),
        },
        {
            "coordinate": "maximal_independent_set_count ** (1/order)",
            "independent_meaning": "finite-tree growth factor",
            "decision": "reject_for_now",
            "reason": (
                "Equivalent information to normalized log at fixed order, with the same lack of "
                "a canonical linear relation to domination and worse exact-arithmetic behavior."
            ),
        },
        {
            "coordinate": "MIS / order-extremal-MIS(order)",
            "independent_meaning": "fraction of the Wilf/Sagan order-wise maximum",
            "decision": "reject_for_now",
            "reason": (
                "This exact bounded normalization has independent extremal meaning, but it mixes "
                "order into the feature and suppresses absolute multiplicity. No exposed structural "
                "argument says domination should be linear in this fraction."
            ),
        },
        {
            "coordinate": "rooted recurrence-state statistic",
            "independent_meaning": "transfer state (A,B,C) for independent domination",
            "decision": "reject_as_single_replacement",
            "reason": (
                "The states explain composition, but depend on a chosen root. Any root-invariant "
                "compression would require a new aggregation choice and would become a bespoke "
                "feature rather than a canonical replacement."
            ),
        },
    ]


def build_diagnosis() -> dict[str, object]:
    rows = [_values(graph) for graph in generate_unlabeled_trees(1, 14)]
    if len(rows) != 5447:
        raise AssertionError("exposed orders 1-14 corpus changed")

    dossier = _candidate_metadata()
    _stability(rows, dossier)

    experiments = _jsonl(EXPERIMENT_REGISTRY)
    tf001028 = [
        row for row in _jsonl(CANDIDATE_REGISTRY) if row["candidate_id"] == "TF-001028"
    ]
    next_id = CandidateRegistry(CANDIDATE_REGISTRY).next_id()
    if [row["revision"] for row in tf001028] != list(range(1, 8)):
        raise AssertionError("TF-001028 lineage changed")
    if tf001028[-1]["lifecycle_state"] != "KNOWN_RESULT":
        raise AssertionError("TF-001028 is not KNOWN_RESULT")
    if next_id != "TF-001158":
        raise AssertionError("candidate-ID continuity changed")
    if sum(row["experiment_id"] == "TF4-0001" for row in experiments) != 1:
        raise AssertionError("TF4-0001 registry multiplicity changed")
    if any(str(row["experiment_id"]).startswith("TF5") for row in experiments):
        raise AssertionError("unexpected TF5 scientific experiment record")

    return {
        "analysis_id": "TF6-DIAG-0001",
        "classification": "EXPOSED_DATA_DIAGNOSIS_ONLY",
        "starting_main_head": STARTING_MAIN,
        "starting_main_ci_run": 37032824545,
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, 14],
            "tf2_tf3_tf4_hostile_sets": "burned",
            "tf5_candidate_specific_family_instances": "burned interpretation data",
        },
        "provenance_verification": {
            "tf2": {
                "source_commit": "d091d88889fa72322bfc49a5531bc30b1f31b049",
                "scientific_run": 36888114138,
            },
            "tf3": {
                "corrected_diagnostic_run": 36907058956,
                "source_commit": "e23b44d24a7b87d6f67aa18749059540934b2767",
                "scientific_run": 36914647703,
            },
            "tf4": {
                "diagnostic_runs": [36972524602, 36973194898],
                "source_commit": "d8e0874a22dde7f226431fc4f15a36adb8254efa",
                "scientific_run": 36983184665,
                "experiment_registry_records": 1,
            },
            "tf5": {
                "pr": 11,
                "final_main_head": STARTING_MAIN,
                "final_main_ci_run": 37032824545,
                "tf001028_final_state": tf001028[-1]["lifecycle_state"],
                "tf001028_final_revision": tf001028[-1]["revision"],
                "tf001028_graduation_candidate": False,
                "scientific_experiment_records": 0,
            },
            "highest_allocated_candidate": "TF-001157",
            "next_permanent_candidate_id": next_id,
        },
        "candidate_fan": {
            "candidate_ids": MIS_IDS,
            "count": len(MIS_IDS),
            "dossier": dossier,
        },
        "geometry": _geometry(rows),
        "structural_recurrence": _structural_diagnosis(rows),
        "transformations_considered": _transformations(),
        "literature_scope": [
            {
                "source": (
                    "Herbert S. Wilf, The Number of Maximal Independent Sets in a Tree, "
                    "SIAM J. Algebraic Discrete Methods 7 (1986), 125-130, "
                    "DOI 10.1137/0607015"
                ),
                "role": "order-wise extremal MIS-count scale",
            },
            {
                "source": (
                    "Bruce E. Sagan, A Note on Independent Sets in Trees, "
                    "SIAM J. Discrete Math. 1 (1988), 105-108, DOI 10.1137/0401012"
                ),
                "role": "simple proof and characterization of the Wilf extremal envelope",
            },
            {
                "source": (
                    "D. S. Taletskii and D. S. Malyshev, The number of maximal independent "
                    "sets in trees with a given number of leaves, Discrete Appl. Math. 314 "
                    "(2022), 321-330, DOI 10.1016/j.dam.2022.03.012"
                ),
                "role": (
                    "structurally conditioned extremal counts; also records the corona/extension "
                    "identity mi(ext(T))=i(T)"
                ),
            },
            {
                "source": (
                    "Maximal independent sets in caterpillar graphs, Discrete Appl. Math. 160 "
                    "(2012), 259-266, DOI 10.1016/j.dam.2011.10.024"
                ),
                "role": "targeted confirmation that MIS enumeration has dedicated caterpillar structure",
            },
        ],
        "decision": {
            "raw_mis_coordinate": "RETAIN_UNCHANGED_FOR_NOW",
            "new_experiment_frozen": False,
            "candidate_ids_allocated": [],
            "experiment_registry_updated": False,
            "reason": (
                "TF6 finds an independent structural explanation for the raw count's scale but no "
                "independently canonical replacement or removal criterion. Log/growth/extremal "
                "normalizations are meaningful diagnostics, not justified discovery coordinates. "
                "The exposed coefficient planes remain stable and equality-supported through order "
                "14, so freezing a new experiment would manufacture an axis rather than diagnose one."
            ),
            "next_session_recommendation": (
                "Keep orders >=15 untouched. If continuing the MIS question, attack the two exposed "
                "support/MIS dominance conditions or derive a root-invariant transfer statistic "
                "independently of candidate yield; otherwise archive the fan and choose a separately "
                "motivated scientific question before freezing another discovery experiment."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = build_diagnosis()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
