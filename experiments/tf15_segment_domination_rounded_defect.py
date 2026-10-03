#!/usr/bin/env python3
"""Reproduce TF15 rounded-defect diagnostics on burned orders 1--14 only."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from functools import cache
from pathlib import Path

import networkx as nx

from experiments.tf12_segment_domination_diagnosis import (
    _maximum_formula,
    domination_number_dp,
)
from experiments.tf13_segment_domination_equality import (
    _tree_description,
    leaf_count,
    maximum_leaf_interval,
)
from experiments.tf14_segment_domination_maximum_equality import (
    fixed_leaf_maximum_branch,
    independent_domination_number_dp,
)
from experiments.tf14_segment_domination_maximum_equality import (
    validate_repository_boundary as validate_tf14_boundary,
)
from treeforge.invariants.core import segment_count
from treeforge.trees.canonical import canonical_tree_code, generate_unlabeled_trees

EXPERIMENTS = Path("data/registry/experiments.jsonl")
TF15_SPEC = Path("experiments/TF15-0001/spec.json")

_DORFLING_OPERATION_DATA = {
    "T1": (1, 0, 1),
    "T2": (2, 1, 1),
    "T3": (2, 1, 1),
    "T4": (3, 1, 1),
    "T5": (3, 1, 1),
    "T6": (5, 2, 2),
}


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def dorfling_defect_increment(operation: str, *, attacher_is_leaf: bool) -> int:
    """Return Delta(n+L-3i) for one valid post-initial Dorfling operation.

    The tuple stored for each operation is
    (new_vertices, increase_in_i, newly_created_leaf_endpoints).
    A pre-existing leaf attacher ceases to be a leaf.
    """
    added_vertices, added_i, new_leaf_endpoints = _DORFLING_OPERATION_DATA[operation]
    delta_leaves = new_leaf_endpoints - int(attacher_is_leaf)
    return added_vertices + delta_leaves - 3 * added_i


def dorfling_defect_transition_table() -> dict[str, dict[str, int]]:
    return {
        operation: {
            "leaf_attacher": dorfling_defect_increment(
                operation, attacher_is_leaf=True
            ),
            "nonleaf_attacher": dorfling_defect_increment(
                operation, attacher_is_leaf=False
            ),
        }
        for operation in _DORFLING_OPERATION_DATA
    }


def _support_parts(graph: nx.Graph) -> tuple[set[int], set[int], set[int]]:
    leaves = {vertex for vertex, degree in graph.degree() if degree == 1}
    supports = {
        vertex
        for vertex in graph.nodes()
        if any(neighbor in leaves for neighbor in graph.neighbors(vertex))
    }
    core = set(graph.nodes()) - leaves - supports
    return leaves, supports, core


def support_link_count(graph: nx.Graph) -> int:
    """Cabrera-Martinez support-link count, for trees of order at least three."""
    _, supports, core = _support_parts(graph)
    return sum(
        any(neighbor in supports for neighbor in graph.neighbors(vertex))
        and all(neighbor in supports for neighbor in graph.neighbors(vertex))
        for vertex in core
    )


def strong_leaf_support_counts(graph: nx.Graph) -> tuple[int, int]:
    """Return (strong leaves, strong supports)."""
    leaves, supports, _ = _support_parts(graph)
    strong_supports = {
        vertex
        for vertex in supports
        if sum(neighbor in leaves for neighbor in graph.neighbors(vertex)) >= 2
    }
    strong_leaves = {
        leaf
        for leaf in leaves
        if next(iter(graph.neighbors(leaf))) in strong_supports
    }
    return len(strong_leaves), len(strong_supports)


def rounded_defect(graph: nx.Graph) -> int:
    """epsilon(T)=n(T)+L(T)-3i(T)."""
    return (
        graph.number_of_nodes()
        + leaf_count(graph)
        - 3 * independent_domination_number_dp(graph)
    )


def _augmented_description(graph: nx.Graph) -> dict[str, object]:
    leaves, supports, core = _support_parts(graph)
    description = _tree_description(graph)
    description.update(
        {
            "canonical_code": canonical_tree_code(graph),
            "domination_number": domination_number_dp(graph),
            "independent_domination_number": independent_domination_number_dp(graph),
            "epsilon": rounded_defect(graph),
            "support_vertex_count": len(supports),
            "support_leaf_excess": len(leaves) - len(supports),
            "support_link_count": support_link_count(graph),
            "non_support_nonleaf_count": len(core),
        }
    )
    return description


def _example_key(graph: nx.Graph) -> tuple[object, ...]:
    return (
        graph.number_of_nodes(),
        segment_count(graph),
        leaf_count(graph),
        canonical_tree_code(graph),
    )


@cache
def build_diagnosis() -> dict[str, object]:
    trees = generate_unlabeled_trees(1, 14)
    assert len(trees) == 5447

    refined_bound_checks = 0
    strong_leaf_identity_checks = 0
    residue_counts: Counter[int] = Counter()
    profile_counts: Counter[tuple[int, int, int]] = Counter()
    profile_examples: dict[tuple[int, int, int], nx.Graph] = {}

    for graph in trees:
        order = graph.number_of_nodes()
        if order < 3:
            continue

        leaves, supports, _ = _support_parts(graph)
        leaves_count = len(leaves)
        support_count = len(supports)
        delta = leaves_count - support_count
        strong_leaves, strong_supports = strong_leaf_support_counts(graph)
        assert strong_leaves - strong_supports == delta
        strong_leaf_identity_checks += 1

        gamma = domination_number_dp(graph)
        links = support_link_count(graph)

        # Cabrera-Martinez (2024):
        # 3 gamma <= n + h - |SL| - (|Ls|-|Ss|) = n+h-|SL|-delta.
        assert 3 * gamma <= order + support_count - links - delta
        refined_bound_checks += 1

        segments = segment_count(graph)
        if segments < 3:
            continue

        lower, upper = maximum_leaf_interval(order, segments)
        if not lower <= leaves_count <= upper:
            continue
        if fixed_leaf_maximum_branch(order, leaves_count) != "ROUNDED_STRICT":
            continue

        maximum = _maximum_formula(order, segments)
        if gamma != maximum:
            continue

        independent_gamma = independent_domination_number_dp(graph)
        epsilon = order + leaves_count - 3 * independent_gamma
        assert gamma == independent_gamma == (order + leaves_count) // 3
        assert epsilon == (order + leaves_count) % 3
        assert epsilon in {0, 1, 2}

        # Combining the 2024 domination bound with
        # 3 gamma = n+L-epsilon = n+h+delta-epsilon gives:
        # 2 delta + |SL| <= epsilon.
        assert 2 * delta + links <= epsilon

        residue_counts[epsilon] += 1
        profile = (epsilon, delta, links)
        profile_counts[profile] += 1
        current = profile_examples.get(profile)
        if current is None or _example_key(graph) < _example_key(current):
            profile_examples[profile] = graph

    assert residue_counts == Counter({0: 49, 1: 119, 2: 49})
    assert profile_counts == Counter(
        {
            (0, 0, 0): 49,
            (1, 0, 0): 50,
            (1, 0, 1): 69,
            (2, 0, 0): 33,
            (2, 0, 1): 3,
            (2, 0, 2): 5,
            (2, 1, 0): 8,
        }
    )

    transition_table = dorfling_defect_transition_table()
    assert transition_table == {
        "T1": {"leaf_attacher": 1, "nonleaf_attacher": 2},
        "T2": {"leaf_attacher": -1, "nonleaf_attacher": 0},
        "T3": {"leaf_attacher": -1, "nonleaf_attacher": 0},
        "T4": {"leaf_attacher": 0, "nonleaf_attacher": 1},
        "T5": {"leaf_attacher": 0, "nonleaf_attacher": 1},
        "T6": {"leaf_attacher": 0, "nonleaf_attacher": 1},
    }

    return {
        "analysis_id": "TF15-DIAG-0001",
        "classification": "ROUNDED_DEFECT_RECURSIVELY_CLASSIFIED_FIXED_SEGMENT_THREAD_CLOSED",
        "starting_main_head": "63fa16c17f04b27b541a3222b10f6c933165aa39",
        "starting_tf14_pr": 20,
        "starting_tf14_pr_head": "4afc22d70df65be24057605ccf164fbfd66b23b8",
        "starting_tf14_pr_head_ci": 37132239373,
        "starting_tf14_post_merge_ci": 37132400796,
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, 14],
            "tree_count": len(trees),
            "orders_at_least_15": "untouched",
        },
        "published_constructive_grammar": {
            "source": (
                "Dorfling-Goddard-Henning-Mynhardt (2006), Theorem 7, "
                "Corollary 9, Observation 11"
            ),
            "base": (
                "Every nontrivial (gamma,i)-tree has some rho-i labeling with a "
                "construction starting from P1 (status D); the mandatory first T1 "
                "produces P2 and changes epsilon from -2 to 1."
            ),
            "defect": "epsilon(T)=n(T)+L(T)-3i(T)",
            "post_initial_transition_table": transition_table,
            "classification": (
                "For a nontrivial tree with gamma=i, any valid P1-starting construction "
                "has epsilon 1 immediately after its first T1. Thereafter epsilon is "
                "updated by the table above. Hence Favaron integer saturation in residue "
                "1 or 2 is equivalent to the construction defect walk ending at 1 or 2."
            ),
        },
        "strict_rounded_residue_1": {
            "status": "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS",
            "characterization": (
                "On the strict rounded branch, T is maximum with n+L congruent to 1 mod 3 "
                "iff T admits the published Dorfling et al. P1-starting (gamma,i) "
                "construction and its defect walk ends at epsilon=1."
            ),
        },
        "strict_rounded_residue_2": {
            "status": "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS",
            "characterization": (
                "On the strict rounded branch, T is maximum with n+L congruent to 2 mod 3 "
                "iff T admits the published Dorfling et al. P1-starting (gamma,i) "
                "construction and its defect walk ends at epsilon=2."
            ),
        },
        "support_refinement": {
            "source": "Cabrera-Martinez (2024) improved domination bound",
            "necessary_condition": "2 delta + |SL(T)| <= epsilon",
            "residue_1_consequence": "delta=0 and |SL(T)|<=1",
            "residue_2_consequence": (
                "either delta=0 and |SL(T)|<=2, or delta=1 and |SL(T)|=0"
            ),
            "equality_in_refined_bound_is_not_necessary": True,
        },
        "burned_diagnostics": {
            "refined_domination_bound_checks": refined_bound_checks,
            "strong_leaf_excess_identity_checks": strong_leaf_identity_checks,
            "strict_rounded_maximizer_residue_counts": {
                str(key): value for key, value in sorted(residue_counts.items())
            },
            "residue_delta_support_link_profiles": {
                f"epsilon={epsilon},delta={delta},support_links={links}": count
                for (epsilon, delta, links), count in sorted(profile_counts.items())
            },
            "smallest_profile_examples": {
                f"epsilon={epsilon},delta={delta},support_links={links}": (
                    _augmented_description(graph)
                )
                for (epsilon, delta, links), graph in sorted(profile_examples.items())
            },
        },
        "prior_art_status": {
            "favaron_real_equality": (
                "Published full equality list covers epsilon=0; no defect-1/2 list was "
                "located in the bounded Favaron/survey/2025-2026 search."
            ),
            "gamma_i_class": (
                "Published exact constructive characterization supplies the ambient class."
            ),
            "negative_search_is_novelty_evidence": False,
        },
        "theorem_significance": (
            "The residue-1/2 result is an exact local bookkeeping corollary of a published "
            "(gamma,i)-tree construction, not a new standalone extremal theory. The "
            "support-link consequence is a useful independent structural restriction, but "
            "burned examples show equality in that refined domination bound is not necessary."
        ),
        "decision": {
            "full_fixed_segment_maximum_equality_complete": True,
            "fixed_segment_thread": "CLOSED",
            "new_experiment_frozen": False,
            "experiment_id": None,
            "scientific_experiment_executed": False,
            "candidate_ids_allocated": [],
            "candidate_registry_changed": False,
            "experiment_registry_changed": False,
            "next_candidate_id": "TF-001158",
            "new_default_invariant_added": False,
            "tf4_mis_fan_reopened": False,
            "tf7_tf9_theorem_thread_reopened": False,
            "order_15_consumed": False,
            "orders_at_least_15_untouched": True,
            "next_session_recommendation": (
                "Return TreeForge to a research-question pause. Do not create TF16 merely "
                "to restate the closed fixed-segment theorem or spend order 15."
            ),
        },
    }


def validate_repository_boundary() -> None:
    validate_tf14_boundary()
    experiments = _jsonl(EXPERIMENTS)
    assert all(
        not str(row["experiment_id"]).startswith("TF15")
        for row in experiments
    )
    assert not TF15_SPEC.exists()


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
