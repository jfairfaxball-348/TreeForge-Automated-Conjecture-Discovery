#!/usr/bin/env python3
"""Reproduce TF14 maximum-equality diagnostics on burned orders 1--14 only."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from functools import cache
from pathlib import Path

import networkx as nx

from experiments.tf12_segment_domination_diagnosis import (
    _maximum_formula,
    domination_number_dp,
)
from experiments.tf13_segment_domination_equality import (
    _tree_description,
    all_nonleaves_are_supports,
    degree_sequence,
    leaf_count,
    maximum_leaf_interval,
    support_vertex_count,
)
from experiments.tf13_segment_domination_equality import (
    validate_repository_boundary as validate_tf13_boundary,
)
from treeforge.invariants.core import segment_count
from treeforge.trees.canonical import canonical_tree_code, generate_unlabeled_trees

EXPERIMENTS = Path("data/registry/experiments.jsonl")
TF14_SPEC = Path("experiments/TF14-0001/spec.json")


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def independent_domination_number_dp(graph: nx.Graph) -> int:
    """Exact rooted-tree DP for the minimum independent dominating set size."""
    root = next(iter(graph.nodes()))
    inf = graph.number_of_nodes() + 1

    def visit(vertex: int, parent: int | None) -> tuple[int, int, int]:
        child_states = [visit(u, vertex) for u in graph.neighbors(vertex) if u != parent]

        # vertex selected: children cannot be selected, and may rely on their parent
        selected = 1 + sum(min(dominated, needs_parent) for _, dominated, needs_parent in child_states)

        # vertex not selected and not dominated below: every child is dominated below
        needs_parent = sum(dominated for _, dominated, _ in child_states)

        # vertex not selected but dominated by at least one selected child
        if not child_states:
            dominated_by_child = inf
        else:
            base = sum(min(selected_child, dominated) for selected_child, dominated, _ in child_states)
            dominated_by_child = (
                base
                if any(selected_child <= dominated for selected_child, dominated, _ in child_states)
                else base
                + min(selected_child - dominated for selected_child, dominated, _ in child_states)
            )
        return selected, dominated_by_child, needs_parent

    selected, dominated, _ = visit(root, None)
    return min(selected, dominated)


def fixed_leaf_maximum_branch(order: int, leaves: int) -> str:
    """Which term is active in min(n-L, floor((n+L)/3))."""
    nonleaves = order - leaves
    rounded = (order + leaves) // 3
    if nonleaves < rounded:
        return "N_MINUS_L_STRICT"
    if rounded < nonleaves:
        return "ROUNDED_STRICT"
    return "TIE"


def _support_core_parts(graph: nx.Graph) -> tuple[set[int], set[int], set[int]]:
    leaves = {vertex for vertex, degree in graph.degree() if degree == 1}
    supports = {
        vertex
        for vertex in graph.nodes()
        if any(neighbor in leaves for neighbor in graph.neighbors(vertex))
    }
    core = set(graph.nodes()) - leaves - supports
    return leaves, supports, core


def support_core_cost(graph: nx.Graph) -> int:
    """Minimum extra core vertices needed once every support vertex is selected."""
    assert graph.number_of_nodes() >= 3
    _, supports, core = _support_core_parts(graph)
    ordered_core = sorted(core)

    def dominates(candidate: set[int]) -> bool:
        return all(
            vertex in candidate
            or any(neighbor in candidate for neighbor in graph.neighbors(vertex))
            for vertex in graph.nodes()
        )

    for size in range(len(ordered_core) + 1):
        for chosen in itertools.combinations(ordered_core, size):
            if dominates(supports | set(chosen)):
                return size
    raise AssertionError("support vertices plus the whole non-support core must dominate")


def support_core_target(graph: nx.Graph) -> int:
    """Rounded-branch target after removing the forced support contribution."""
    leaves, supports, core = _support_core_parts(graph)
    leaf_excess = len(leaves) - len(supports)
    return (len(core) + 2 * leaf_excess) // 3


def kurnosov_theorem3_sufficient_condition(graph: nx.Graph) -> str | None:
    """Return which of Kurnosov 2020 Theorem 3's two sufficient cases applies."""
    if graph.number_of_nodes() < 3:
        return None
    leaves, supports, core = _support_core_parts(graph)
    nonleaves = set(graph.nodes()) - leaves

    if nonleaves <= supports:
        return "EVERY_NONLEAF_SUPPORT"

    one_leaf_per_support = all(
        sum(neighbor in leaves for neighbor in graph.neighbors(vertex)) == 1
        for vertex in supports
    )
    core_degree_two = all(graph.degree(vertex) == 2 for vertex in core)
    core_is_path = False
    if core:
        induced = graph.subgraph(core)
        core_is_path = nx.is_connected(induced) and all(
            degree <= 2 for _, degree in induced.degree()
        )

    if one_leaf_per_support and core_degree_two and core_is_path:
        return "ONE_LEAF_PER_SUPPORT_DEGREE2_CORE_PATH"
    return None


def _core_is_linear_forest(graph: nx.Graph) -> bool:
    _, _, core = _support_core_parts(graph)
    return all(degree <= 2 for _, degree in graph.subgraph(core).degree())


def _augmented_tree_description(graph: nx.Graph) -> dict[str, object]:
    leaves, supports, core = _support_core_parts(graph)
    induced = graph.subgraph(core)
    components = (
        sorted((len(component) for component in nx.connected_components(induced)), reverse=True)
        if core
        else []
    )
    description = _tree_description(graph)
    description.update(
        {
            "independent_domination_number": independent_domination_number_dp(graph),
            "support_leaf_excess": len(leaves) - len(supports),
            "non_support_nonleaf_count": len(core),
            "non_support_nonleaf_component_orders": components,
            "non_support_nonleaf_degrees_in_tree": sorted(
                (graph.degree(vertex) for vertex in core), reverse=True
            ),
            "support_core_cost": support_core_cost(graph),
            "support_core_target": support_core_target(graph),
        }
    )
    return description


def _example_sort_key(graph: nx.Graph) -> tuple[object, ...]:
    return (
        graph.number_of_nodes(),
        segment_count(graph),
        leaf_count(graph),
        degree_sequence(graph),
        canonical_tree_code(graph),
    )


@cache
def build_diagnosis() -> dict[str, object]:
    trees = generate_unlabeled_trees(1, 14)
    assert len(trees) == 5447

    groups: dict[tuple[int, int], list[tuple[int, int, nx.Graph]]] = defaultdict(list)
    support_core_identity_checks = 0
    independent_domination_bound_checks = 0

    for graph in trees:
        order = graph.number_of_nodes()
        segments = segment_count(graph)
        gamma = domination_number_dp(graph)
        independent_gamma = independent_domination_number_dp(graph)
        groups[(order, segments)].append((gamma, independent_gamma, graph))

        if order >= 2:
            leaves = leaf_count(graph)
            assert gamma <= independent_gamma <= (order + leaves) // 3
            independent_domination_bound_checks += 1

        if order >= 3:
            supports = support_vertex_count(graph)
            assert gamma == supports + support_core_cost(graph)
            support_core_identity_checks += 1

    branch_maximizer_counts: Counter[str] = Counter()
    strict_rounded_residue_counts: Counter[int] = Counter()
    strict_rounded_eligible_residue_counts: Counter[str] = Counter()
    kurnosov_sufficient_counts: Counter[str] = Counter()
    strict_rounded_maximizers: list[nx.Graph] = []

    for (order, segments), rows in sorted(groups.items()):
        values = [gamma for gamma, _, _ in rows]
        maximum = max(values)
        assert maximum == _maximum_formula(order, segments)

        if segments < 3:
            continue

        lower, upper = maximum_leaf_interval(order, segments)
        for gamma, independent_gamma, graph in rows:
            leaves = leaf_count(graph)
            if not lower <= leaves <= upper:
                continue

            branch = fixed_leaf_maximum_branch(order, leaves)
            rounded = (order + leaves) // 3

            if branch in {"N_MINUS_L_STRICT", "TIE"}:
                assert (gamma == maximum) == all_nonleaves_are_supports(graph)

            if branch != "ROUNDED_STRICT":
                if gamma == maximum:
                    branch_maximizer_counts[branch] += 1
                continue

            residue = (order + leaves) % 3
            is_maximizer = gamma == maximum
            strict_rounded_eligible_residue_counts[
                f"residue_{residue}_{'max' if is_maximizer else 'nonmax'}"
            ] += 1

            # Favaron's bound and gamma <= i make this an exact iff reduction.
            assert is_maximizer == (
                gamma == independent_gamma == rounded == maximum
            )

            # Equivalent support-core formulation.
            target = support_core_target(graph)
            assert is_maximizer == (support_core_cost(graph) == target)

            if not is_maximizer:
                continue

            branch_maximizer_counts[branch] += 1
            strict_rounded_residue_counts[residue] += 1
            strict_rounded_maximizers.append(graph)

            condition = kurnosov_theorem3_sufficient_condition(graph)
            kurnosov_sufficient_counts[
                condition if condition is not None else "OUTSIDE_THEOREM3_SUFFICIENT_CASES"
            ] += 1

    assert strict_rounded_maximizers

    outside_kurnosov = [
        graph
        for graph in strict_rounded_maximizers
        if kurnosov_theorem3_sufficient_condition(graph) is None
    ]
    repeated_support_leaf = [
        graph
        for graph in strict_rounded_maximizers
        if leaf_count(graph) > support_vertex_count(graph)
    ]
    nonlinear_core = [
        graph for graph in strict_rounded_maximizers if not _core_is_linear_forest(graph)
    ]

    assert outside_kurnosov
    assert repeated_support_leaf
    assert nonlinear_core

    smallest_outside_kurnosov = min(outside_kurnosov, key=_example_sort_key)
    smallest_repeated_support_leaf = min(repeated_support_leaf, key=_example_sort_key)
    smallest_nonlinear_core = min(nonlinear_core, key=_example_sort_key)

    return {
        "analysis_id": "TF14-DIAG-0001",
        "classification": "MAXIMUM_PARTIALLY_RESOLVED_ROUNDED_SLACK_RESIDUE_ISOLATED",
        "starting_main_head": "8213e511715f478f7f0e94f89902e6aa076a4a15",
        "starting_tf13_pr": 19,
        "starting_tf13_pr_head": "c48a2362ba4367278dc8b83469927edf10c5943d",
        "starting_tf13_pr_head_ci": 37129172222,
        "starting_tf13_post_merge_ci": 37129314891,
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, 14],
            "tree_count": len(trees),
            "orders_at_least_15": "untouched",
        },
        "tf13_materialization_note": {
            "requested_committed_path": "experiments/TF13-DIAG-0001/diagnosis.json",
            "present_at_starting_main": False,
            "deterministic_reproducer_present": True,
            "scientific_consequence": "none",
        },
        "prior_art_audit": {
            "gentner_henning_rautenbach_2016": {
                "theorem": "Theorem 3; Lemma 2 and the edge-switch claims in its proof",
                "finding": (
                    "Determines the maximum value for a fixed forest degree sequence and "
                    "constructs/canonicalizes an attaining realization; the proof does not "
                    "state an iff characterization of every maximizing realization."
                ),
            },
            "kurnosov_2020": {
                "theorems": "Theorem 3, Remark 1, Lemma 5, Theorem 7",
                "finding": (
                    "Theorem 3 gives two sufficient maximum-realization structures. Remark 1 "
                    "explicitly says they are not necessary and supplies an infinite maximum "
                    "family outside them. Lemma 5 and Theorem 7 provide degree-sequence-preserving "
                    "moves and interval reachability, not a no-move iff criterion for maxima."
                ),
            },
            "favaron_1992": {
                "theorem": "i(T) <= (n+L)/3, with the real-equality trees characterized",
                "finding": (
                    "Closes the strict rounded branch only when n+L is divisible by 3; the "
                    "located equality classification is for i(T)=(n+L)/3, not the residue-1/2 "
                    "integer saturation i(T)=floor((n+L)/3)."
                ),
            },
            "gamma_i_tree_literature": {
                "sources": (
                    "Cockayne-Favaron-Mynhardt-Puech (2000); "
                    "Dorfling-Goddard-Henning-Mynhardt (2006)"
                ),
                "finding": (
                    "Trees with gamma(T)=i(T) have published exact and constructive "
                    "characterizations."
                ),
            },
            "later_fixed_degree_sequence_work": {
                "source": "Krupoderova-Kurnosov (2025)",
                "finding": (
                    "The located later comparison concerns minimum-domination/support extremizers, "
                    "not a complete classification of maximum-domination realizations."
                ),
            },
            "negative_search_is_novelty_evidence": False,
        },
        "maximum_equality": {
            "overall_status": "PARTIALLY_RESOLVED",
            "n_minus_l_strict_status": "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS",
            "tie_status": "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS",
            "n_minus_l_or_tie_characterization": (
                "For every optimizing leaf count with n-L <= floor((n+L)/3), "
                "gamma(T)=M iff every nonleaf vertex is a support vertex."
            ),
            "strict_rounded_reduction_status": "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS",
            "strict_rounded_reduction": (
                "For an optimizing leaf count with floor((n+L)/3)<n-L, "
                "gamma(T)=M iff gamma(T)=i(T)=floor((n+L)/3)."
            ),
            "strict_rounded_residue_0_status": "DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATIONS",
            "strict_rounded_residue_0_characterization": (
                "When n+L is 0 modulo 3, strict-rounded maximizers are exactly the "
                "intersection of Favaron's equality trees i(T)=(n+L)/3 with the published "
                "(gamma,i)-trees."
            ),
            "strict_rounded_residue_1_2_status": "UNRESOLVED_AFTER_BOUNDED_AUDIT",
            "strict_rounded_residue_1_2_residue": (
                "Characterize the published (gamma,i)-trees that satisfy "
                "i(T)=floor((n+L)/3) when n+L is 1 or 2 modulo 3."
            ),
            "support_core_exact_reduction": (
                "Let H be the support vertices, S the nonleaf non-support vertices, "
                "delta=L-|H|, and tau the minimum |X| for X subset S such that H union X "
                "dominates T. Then gamma(T)=|H|+tau. On the strict rounded branch, "
                "maximality is equivalent to tau=floor((|S|+2 delta)/3)."
            ),
        },
        "burned_diagnostics": {
            "support_core_identity_checks": support_core_identity_checks,
            "independent_domination_bound_checks": independent_domination_bound_checks,
            "branch_maximizer_counts_q_at_least_3": dict(sorted(branch_maximizer_counts.items())),
            "strict_rounded_maximizer_residue_counts": {
                str(key): value for key, value in sorted(strict_rounded_residue_counts.items())
            },
            "strict_rounded_eligible_residue_counts": dict(
                sorted(strict_rounded_eligible_residue_counts.items())
            ),
            "kurnosov_theorem3_sufficient_counts_on_strict_rounded_maximizers": dict(
                sorted(kurnosov_sufficient_counts.items())
            ),
            "smallest_strict_rounded_maximizer_outside_kurnosov_theorem3_sufficient_cases": (
                _augmented_tree_description(smallest_outside_kurnosov)
            ),
            "smallest_strict_rounded_maximizer_with_multiple_leaves_at_a_support": (
                _augmented_tree_description(smallest_repeated_support_leaf)
            ),
            "smallest_strict_rounded_maximizer_with_nonlinear_non_support_core": (
                _augmented_tree_description(smallest_nonlinear_core)
            ),
        },
        "theorem_significance": (
            "TF14 sharpens the realization problem substantially but does not produce a complete "
            "new classification. The residue-0 rounded case is a short intersection of published "
            "classifications; the residue-1/2 support-core reduction is elementary and should "
            "remain inside TreeForge unless a later session proves a genuinely structural iff."
        ),
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
                "If the fixed-segment maximum question continues, attack only the strict-rounded "
                "residue-1/2 saturation problem, preferably through the support-core partial "
                "domination formulation or the published constructive (gamma,i)-tree grammar."
            ),
        },
    }


def validate_repository_boundary() -> None:
    validate_tf13_boundary()
    experiments = _jsonl(EXPERIMENTS)
    assert all(
        not str(row["experiment_id"]).startswith("TF14")
        for row in experiments
    )
    assert not TF14_SPEC.exists()


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
