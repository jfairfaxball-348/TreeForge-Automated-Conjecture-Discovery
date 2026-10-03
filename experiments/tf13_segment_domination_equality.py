#!/usr/bin/env python3
"""Reproduce TF13 fixed-segment domination equality diagnostics on burned orders 1--14."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from functools import cache
from pathlib import Path

import networkx as nx

from experiments.tf12_segment_domination_diagnosis import (
    _maximum_formula,
    _minimum_formula,
    _minimum_leaf_count,
    _segment_paths,
    domination_number_dp,
)
from experiments.tf12_segment_domination_diagnosis import (
    validate_repository_boundary as validate_tf12_boundary,
)
from treeforge.invariants.core import segment_count
from treeforge.trees.canonical import canonical_tree_code, generate_unlabeled_trees

EXPERIMENTS = Path("data/registry/experiments.jsonl")
TF13_SPEC = Path("experiments/TF13-0001/spec.json")


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def leaf_count(graph: nx.Graph) -> int:
    if graph.number_of_nodes() == 1:
        return 0
    return sum(degree == 1 for _, degree in graph.degree())


def support_vertex_count(graph: nx.Graph) -> int:
    leaves = {vertex for vertex, degree in graph.degree() if degree == 1}
    return sum(
        any(neighbor in leaves for neighbor in graph.neighbors(vertex))
        for vertex in graph.nodes()
    )


def all_nonleaves_are_supports(graph: nx.Graph) -> bool:
    """Return the structural condition for gamma(T)=n-L, for order at least 3."""
    leaves = {vertex for vertex, degree in graph.degree() if degree == 1}
    supports = {
        vertex
        for vertex in graph.nodes()
        if any(neighbor in leaves for neighbor in graph.neighbors(vertex))
    }
    return all(vertex in supports for vertex in graph.nodes() if vertex not in leaves)


def degree_sequence(graph: nx.Graph) -> tuple[int, ...]:
    return tuple(sorted((degree for _, degree in graph.degree()), reverse=True))


def minimum_ceiling_slack(order: int, segments: int) -> int:
    """Slack r in 3 ceil((n-q+2)/3) = n-q+2+r."""
    assert segments >= 3
    value = _minimum_formula(order, segments)
    slack = 3 * value - (order - segments + 2)
    assert slack in {0, 1, 2}
    return slack


def minimum_equality_classes(order: int, segments: int) -> list[dict[str, int]]:
    """Published G_0^m classes eligible to attain the fixed-(n,q) minimum."""
    assert segments >= 3
    slack = minimum_ceiling_slack(order, segments)
    minimum_leaves = _minimum_leaf_count(segments)
    maximum_deficit = min(slack, segments - minimum_leaves)
    return [
        {
            "leaf_deficit_from_q": deficit,
            "leaf_count": segments - deficit,
            "published_class_index_m": slack - deficit,
        }
        for deficit in range(maximum_deficit + 1)
    ]


def maximum_leaf_interval(order: int, segments: int) -> tuple[int, int]:
    """Complete integer interval of leaf counts attaining the fixed-(n,q) maximum."""
    assert segments >= 3
    maximum = _maximum_formula(order, segments)
    lower = max(_minimum_leaf_count(segments), 3 * maximum - order)
    upper = min(segments, order - maximum)
    assert lower <= upper
    return lower, upper


def _partitions(total: int, parts: int, minimum: int = 1) -> list[tuple[int, ...]]:
    """Nondecreasing positive partitions of total into exactly parts parts."""
    if parts == 0:
        return [()] if total == 0 else []
    if parts == 1:
        return [(total,)] if total >= minimum else []
    result: list[tuple[int, ...]] = []
    largest_first = total // parts
    for first in range(minimum, largest_first + 1):
        for tail in _partitions(total - first, parts - 1, first):
            result.append((first, *tail))
    return result


def admissible_degree_sequences(
    order: int, segments: int, leaves: int
) -> set[tuple[int, ...]]:
    """All tree degree sequences with fixed (n,q,L), via branch excesses."""
    assert segments >= 3
    branch_vertices = segments + 1 - leaves
    degree2_vertices = order - segments - 1
    if branch_vertices < 1 or degree2_vertices < 0:
        return set()
    sequences: set[tuple[int, ...]] = set()
    for excesses in _partitions(leaves - 2, branch_vertices):
        degrees = (
            [2 + excess for excess in excesses]
            + [2] * degree2_vertices
            + [1] * leaves
        )
        sequences.add(tuple(sorted(degrees, reverse=True)))
    return sequences


def leaf_distances_are_two_mod_three(graph: nx.Graph) -> bool:
    leaves = [vertex for vertex, degree in graph.degree() if degree == 1]
    return all(
        nx.shortest_path_length(graph, leaves[i], leaves[j]) % 3 == 2
        for i in range(len(leaves))
        for j in range(i + 1, len(leaves))
    )


def _tree_description(graph: nx.Graph) -> dict[str, object]:
    return {
        "identity": [graph.number_of_nodes(), canonical_tree_code(graph)],
        "degree_sequence": list(degree_sequence(graph)),
        "leaf_count": leaf_count(graph),
        "support_vertex_count": support_vertex_count(graph),
        "segment_lengths": sorted(
            (len(path) - 1 for path in _segment_paths(graph)),
            reverse=True,
        ),
        "edges": sorted(
            [sorted((int(u), int(v))) for u, v in graph.edges()],
        ),
    }


@cache
def build_diagnosis() -> dict[str, object]:
    trees = generate_unlabeled_trees(1, 14)
    assert len(trees) == 5447

    groups: dict[tuple[int, int], list[tuple[int, nx.Graph]]] = defaultdict(list)
    nonleaf_branch_checks = 0
    for graph in trees:
        order = graph.number_of_nodes()
        segments = segment_count(graph)
        gamma = domination_number_dp(graph)
        groups[(order, segments)].append((gamma, graph))

        if order >= 3:
            leaves = leaf_count(graph)
            assert (gamma == order - leaves) == all_nonleaves_are_supports(graph)
            nonleaf_branch_checks += 1

        if segments >= 3:
            leaves = leaf_count(graph)
            branch_vertices = sum(degree >= 3 for _, degree in graph.degree())
            degree2_vertices = sum(degree == 2 for _, degree in graph.degree())
            assert branch_vertices == segments + 1 - leaves
            assert degree2_vertices == order - segments - 1
            assert sum(
                degree - 2 for _, degree in graph.degree() if degree >= 3
            ) == leaves - 2

    minimum_residual_counts = {0: 0, 1: 0, 2: 0}
    minimum_leaf_deficit_counts: dict[str, int] = defaultdict(int)
    all_max_leaf_intervals_match = True
    all_max_degree_sequence_sets_match = True
    mixed_degree_sequence_groups: list[
        tuple[int, int, tuple[int, ...], list[tuple[int, nx.Graph]]]
    ] = []
    nonstar_minimum_example: dict[str, object] | None = None

    for (order, segments), rows in sorted(groups.items()):
        values = [gamma for gamma, _ in rows]
        minimum = min(values)
        maximum = max(values)
        assert minimum == _minimum_formula(order, segments)
        assert maximum == _maximum_formula(order, segments)

        if segments < 3:
            continue

        eligible = {
            (item["leaf_count"], item["published_class_index_m"])
            for item in minimum_equality_classes(order, segments)
        }
        for gamma, graph in rows:
            if gamma != minimum:
                continue
            leaves = leaf_count(graph)
            residual = 3 * gamma - (order - leaves + 2)
            assert (leaves, residual) in eligible
            assert residual in {0, 1, 2}
            minimum_residual_counts[residual] += 1
            deficit = segments - leaves
            minimum_leaf_deficit_counts[
                f"d={deficit},r={minimum_ceiling_slack(order, segments)}"
            ] += 1
            assert leaf_distances_are_two_mod_three(graph) == (residual == 0)

            reduced_branch_vertices = sum(
                degree >= 3 for _, degree in graph.degree()
            )
            if nonstar_minimum_example is None and reduced_branch_vertices >= 2:
                nonstar_minimum_example = {
                    "order": order,
                    "segment_count": segments,
                    "domination_number": gamma,
                    "ceiling_slack": minimum_ceiling_slack(order, segments),
                    "published_class_index_m": residual,
                    "tree": _tree_description(graph),
                }

        lower, upper = maximum_leaf_interval(order, segments)
        predicted_leaves = list(range(lower, upper + 1))
        observed_leaves = sorted(
            {
                leaf_count(graph)
                for gamma, graph in rows
                if gamma == maximum
            }
        )
        all_max_leaf_intervals_match &= observed_leaves == predicted_leaves
        assert observed_leaves == predicted_leaves

        predicted_degree_sequences: set[tuple[int, ...]] = set()
        for leaves in predicted_leaves:
            predicted_degree_sequences.update(
                admissible_degree_sequences(order, segments, leaves)
            )
        observed_max_degree_sequences = {
            degree_sequence(graph)
            for gamma, graph in rows
            if gamma == maximum
        }
        all_max_degree_sequence_sets_match &= (
            observed_max_degree_sequences == predicted_degree_sequences
        )
        assert observed_max_degree_sequences == predicted_degree_sequences

        degree_groups: dict[tuple[int, ...], list[tuple[int, nx.Graph]]] = defaultdict(list)
        for gamma, graph in rows:
            degree_groups[degree_sequence(graph)].append((gamma, graph))
        for sequence, degree_rows in degree_groups.items():
            degree_values = {gamma for gamma, _ in degree_rows}
            if maximum in degree_values and min(degree_values) < maximum:
                mixed_degree_sequence_groups.append(
                    (order, segments, sequence, degree_rows)
                )

    assert nonstar_minimum_example is not None
    assert mixed_degree_sequence_groups
    mixed_degree_sequence_groups.sort(key=lambda item: (item[0], item[1], item[2]))
    order, segments, sequence, degree_rows = mixed_degree_sequence_groups[0]
    maximum = _maximum_formula(order, segments)
    lower_row = min(degree_rows, key=lambda row: row[0])
    upper_row = next(row for row in degree_rows if row[0] == maximum)
    assert (order, segments, sequence) == (6, 3, (3, 2, 2, 1, 1, 1))

    return {
        "analysis_id": "TF13-DIAG-0001",
        "classification": "MINIMUM_CLASSIFIED_MAXIMUM_PARTIALLY_RESOLVED_EXPERIMENT_PAUSED",
        "starting_main_head": "8d0c82567282d2bd2a3a571944cdf084e149439d",
        "starting_post_merge_ci": 37112600371,
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, 14],
            "tree_count": 5447,
            "occupied_n_q_cells": len(groups),
            "orders_at_least_15": "untouched",
        },
        "minimum_equality": {
            "status": "DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATION",
            "published_classification": (
                "Hajian-Henning-Jafari Rad, Theorem 1 (cactus classification), "
                "specialized to k=0 trees; G_0^0 is Lemanska's equality family"
            ),
            "fixed_n_q_characterization": (
                "Let M=ceil((n-q+2)/3), r=3M-(n-q+2), and a=ceil((q+3)/2). "
                "A q>=3 tree is a fixed-(n,q) minimizer iff for some "
                "0<=d<=min(r,q-a), it has L=q-d leaves and belongs to G_0^(r-d)."
            ),
            "lemanska_real_equality": (
                "The residual m=0 class is exactly G_0^0=R, equivalently every "
                "pair of distinct leaves has distance 2 modulo 3."
            ),
            "burned_residual_class_counts": minimum_residual_counts,
            "burned_leaf_deficit_slack_counts": dict(
                sorted(minimum_leaf_deficit_counts.items())
            ),
            "nonstar_reduced_tree_minimizer_exists": True,
            "smallest_recorded_nonstar_example": nonstar_minimum_example,
        },
        "maximum_equality": {
            "status": "PARTIALLY_RESOLVED",
            "optimizing_leaf_counts_status": "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS",
            "optimizing_leaf_counts": (
                "If M=gamma_max(n,q) and a=ceil((q+3)/2), then "
                "L_max(n,q)={L integer: max(a,3M-n)<=L<=min(q,n-M)}."
            ),
            "degree_sequence_capability_status": "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS",
            "degree_sequence_capability": (
                "For every L in L_max, every admissible fixed-(n,q,L) tree degree "
                "sequence has at least one realization with domination M by "
                "Gentner-Henning-Rautenbach Theorem 3."
            ),
            "n_minus_l_branch_status": "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS",
            "n_minus_l_branch": (
                "For every tree of order at least 3, gamma(T)=n-L iff every "
                "nonleaf vertex is a support vertex."
            ),
            "all_tree_isomorphism_classes_status": "UNRESOLVED_AFTER_BOUNDED_AUDIT",
            "obstruction": (
                "A degree sequence can have both maximizing and nonmaximizing tree "
                "realizations, so fixed-degree-sequence attainability is not an iff "
                "classification of all maximizing tree isomorphism classes."
            ),
            "burned_mixed_degree_sequence_group_count": len(mixed_degree_sequence_groups),
            "smallest_mixed_degree_sequence_example": {
                "order": order,
                "segment_count": segments,
                "degree_sequence": list(sequence),
                "fixed_cell_maximum": maximum,
                "nonmaximizer": {
                    "domination_number": lower_row[0],
                    "tree": _tree_description(lower_row[1]),
                },
                "maximizer": {
                    "domination_number": upper_row[0],
                    "tree": _tree_description(upper_row[1]),
                },
            },
        },
        "burned_diagnostics": {
            "all_maximizing_leaf_intervals_match": all_max_leaf_intervals_match,
            "all_capable_degree_sequence_sets_match": all_max_degree_sequence_sets_match,
            "gamma_equals_n_minus_l_iff_all_nonleaves_support_checks": nonleaf_branch_checks,
        },
        "theorem_significance": {
            "minimum": (
                "A short specialization and arithmetic corollary of a published "
                "classification; keep inside TreeForge."
            ),
            "maximum": (
                "The leaf optimizer and n-L branch lemma are useful elementary "
                "reductions, but the complete isomorphism classification remains "
                "unresolved; no theorem-focused repository is justified."
            ),
        },
        "decision": {
            "new_experiment_frozen": False,
            "experiment_id": None,
            "scientific_experiment_executed": False,
            "candidate_ids_allocated": [],
            "candidate_registry_changed": False,
            "experiment_registry_changed": False,
            "next_candidate_id": "TF-001158",
            "tf4_mis_fan_reopened": False,
            "tf7_tf9_theorem_thread_reopened": False,
            "order_15_consumed": False,
            "orders_at_least_15_untouched": True,
            "next_session_recommendation": (
                "If the fixed-segment question continues, remain theorem-first: audit or "
                "derive the full realization-level equality class for the rounded "
                "fixed-leaf upper branch before considering any new experiment."
            ),
        },
    }


def validate_repository_boundary() -> None:
    validate_tf12_boundary()
    experiments = _jsonl(EXPERIMENTS)
    assert all(
        not str(row["experiment_id"]).startswith("TF13")
        for row in experiments
    )
    assert not TF13_SPEC.exists()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    validate_repository_boundary()
    payload = build_diagnosis()
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
