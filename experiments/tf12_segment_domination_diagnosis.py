#!/usr/bin/env python3
"""Reproduce TF12 fixed-segment domination diagnostics on burned orders 1--14 only."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from functools import cache
from pathlib import Path

import networkx as nx

from experiments.tf8_fixed_support_equality import TF4_MIS_FAN
from treeforge.invariants.core import (
    _segment_count_by_decomposition,
    domination_number,
    segment_count,
)
from treeforge.invariants.registry import default_registry
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import canonical_tree_code, generate_unlabeled_trees

CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")
TF12_SPEC = Path("experiments/TF12-0001/spec.json")


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def domination_number_dp(graph: nx.Graph) -> int:
    """Exact three-state tree DP independent of the core exhaustive routine."""
    root = next(iter(graph.nodes()))
    inf = graph.number_of_nodes() + 1

    def visit(vertex: int, parent: int | None) -> tuple[int, int, int]:
        child_states = [visit(u, vertex) for u in graph.neighbors(vertex) if u != parent]
        selected = 1 + sum(min(a, b, c) for a, b, c in child_states)
        needs_parent = sum(b for _, b, _ in child_states)
        if not child_states:
            dominated_by_child = inf
        else:
            base = sum(min(a, b) for a, b, _ in child_states)
            dominated_by_child = (
                base
                if any(a <= b for a, b, _ in child_states)
                else base + min(a - b for a, b, _ in child_states)
            )
        return selected, dominated_by_child, needs_parent

    selected, dominated, _ = visit(root, None)
    return min(selected, dominated)


def _segment_paths(graph: nx.Graph) -> list[list[int]]:
    if graph.number_of_nodes() == 1:
        return []
    endpoints = {v for v, degree in graph.degree() if degree != 2}
    seen: set[frozenset[int]] = set()
    paths: list[list[int]] = []
    for start in endpoints:
        for neighbor in graph.neighbors(start):
            edge = frozenset((start, neighbor))
            if edge in seen:
                continue
            seen.add(edge)
            path = [start]
            previous, current = start, neighbor
            while current not in endpoints:
                path.append(current)
                nxt = next(v for v in graph.neighbors(current) if v != previous)
                seen.add(frozenset((current, nxt)))
                previous, current = current, nxt
            path.append(current)
            paths.append(path)
    assert len(seen) == graph.number_of_edges()
    return paths


def _reduced_tree(graph: nx.Graph) -> nx.Graph:
    if graph.number_of_nodes() == 1:
        return nx.empty_graph(1)
    endpoints = list(v for v, degree in graph.degree() if degree != 2)
    index = {v: i for i, v in enumerate(endpoints)}
    reduced = nx.Graph()
    reduced.add_nodes_from(range(len(endpoints)))
    for path in _segment_paths(graph):
        reduced.add_edge(index[path[0]], index[path[-1]])
    assert nx.is_tree(reduced)
    return reduced


def _tree_description(graph: nx.Graph) -> dict[str, object]:
    reduced = _reduced_tree(graph)
    return {
        "identity": [graph.number_of_nodes(), canonical_tree_code(graph)],
        "leaf_count": 0
        if graph.number_of_nodes() == 1
        else sum(degree == 1 for _, degree in graph.degree()),
        "branch_vertex_count": sum(degree >= 3 for _, degree in graph.degree()),
        "segment_lengths": sorted(
            (len(path) - 1 for path in _segment_paths(graph)),
            reverse=True,
        ),
        "reduced_tree_identity": [
            reduced.number_of_nodes(),
            canonical_tree_code(reduced),
        ],
    }


@cache
def _minimum_formula(order: int, segments: int) -> int:
    if (order, segments) == (1, 0):
        return 1
    if segments == 1:
        return (order + 2) // 3
    if segments >= 3:
        return (order - segments + 4) // 3
    raise AssertionError("segment count 2 is impossible for a tree")


def _minimum_leaf_count(segments: int) -> int:
    return (segments + 4) // 2


def _maximum_formula(order: int, segments: int) -> int:
    if (order, segments) == (1, 0):
        return 1
    if segments == 1:
        return (order + 2) // 3
    if segments >= 3:
        return min(
            order // 2,
            (order + segments) // 3,
            order - _minimum_leaf_count(segments),
        )
    raise AssertionError("segment count 2 is impossible for a tree")


@cache
def _diagnostic_cells() -> list[dict[str, object]]:
    groups: dict[tuple[int, int], list[tuple[int, nx.Graph]]] = defaultdict(list)
    trees = generate_unlabeled_trees(1, 14)
    assert len(trees) == 5447

    for graph in trees:
        q = segment_count(graph)
        assert q == _segment_count_by_decomposition(graph)
        gamma = domination_number_dp(graph)
        if graph.number_of_nodes() <= 8:
            assert gamma == domination_number(graph)
        groups[(graph.number_of_nodes(), q)].append((gamma, graph))

    cells: list[dict[str, object]] = []
    for (order, q), rows in sorted(groups.items()):
        values = [gamma for gamma, _ in rows]
        minimum = min(values)
        maximum = max(values)
        minimizers = [graph for gamma, graph in rows if gamma == minimum]
        maximizers = [graph for gamma, graph in rows if gamma == maximum]
        minimizers.sort(key=canonical_tree_code)
        maximizers.sort(key=canonical_tree_code)

        assert minimum == _minimum_formula(order, q)
        assert maximum == _maximum_formula(order, q)

        cell: dict[str, object] = {
            "order": order,
            "segment_count": q,
            "tree_count": len(rows),
            "minimum_domination_number": minimum,
            "maximum_domination_number": maximum,
            "minimizer_count": len(minimizers),
            "maximizer_count": len(maximizers),
            "representative_minimizer": _tree_description(minimizers[0]),
            "representative_maximizer": _tree_description(maximizers[0]),
        }
        if q >= 3:
            feasible_leaves = range(_minimum_leaf_count(q), q + 1)
            predicted = max(
                min(order - leaves, (order + leaves) // 3)
                for leaves in feasible_leaves
            )
            maximizing_leaves = [
                leaves
                for leaves in feasible_leaves
                if min(order - leaves, (order + leaves) // 3) == predicted
            ]
            observed = sorted(
                {
                    sum(degree == 1 for _, degree in graph.degree())
                    for gamma, graph in rows
                    if gamma == maximum
                }
            )
            assert observed == maximizing_leaves
            cell["maximizing_leaf_counts"] = observed
        cells.append(cell)

    assert len(cells) == 80
    assert not any(cell["segment_count"] == 2 for cell in cells)
    return cells


def build_diagnosis() -> dict[str, object]:
    cells = _diagnostic_cells()
    return {
        "analysis_id": "TF12-DIAG-0001",
        "classification": "PRIOR_ART_VALUE_RESOLUTION_EXPERIMENT_PAUSED",
        "starting_main_head": "ca3d12661c6c6260b7489f8b9efb94416e698452",
        "starting_main_ci_run": 37109895238,
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, 14],
            "orders_at_least_15": "untouched",
        },
        "selected_question": (
            "For finite trees of order n with exactly q segments, determine the minimum "
            "and maximum domination numbers and characterize the extremal trees."
        ),
        "segment_count": {
            "formula": "n - n2 - 1",
            "structural_definition": (
                "number of maximal paths with degree-not-2 endpoints and degree-2 interiors; "
                "equivalently the number of edges after suppressing all degree-2 vertices"
            ),
            "independent_checker": "explicit maximal degree-2 path decomposition",
            "burned_tree_agreement_count": 5447,
        },
        "prior_art_status": {
            "overall": "PARTIALLY_COVERED",
            "minimum_value": "DIRECT_COROLLARY_PLUS_ELEMENTARY_ATTAINMENT",
            "maximum_value": "DIRECT_COROLLARY_PLUS_FINITE_PARAMETER_OPTIMIZATION",
            "complete_extremizer_classification": "NOT_LOCATED_IN_BOUNDED_SEARCH",
            "negative_search_is_novelty_evidence": False,
        },
        "mathematical_reduction": {
            "admissible_segment_counts": "q=0 only for K1; q=1 for nontrivial paths; q=2 impossible; q>=3 possible",
            "degree2_count": "n2=n-q-1",
            "leaf_range_for_q_at_least_3": "ceil((q+3)/2) <= leaves <= q",
            "minimum_formula": (
                "gamma_min(1,0)=1; gamma_min(n,1)=ceil(n/3); "
                "gamma_min(n,q)=ceil((n-q+2)/3) for q>=3"
            ),
            "maximum_formula": (
                "gamma_max(1,0)=1; gamma_max(n,1)=ceil(n/3); "
                "gamma_max(n,q)=min(floor(n/2), floor((n+q)/3), "
                "n-ceil((q+3)/2)) for q>=3"
            ),
            "minimum_source_mechanism": (
                "Lemanska's gamma >= (n+2-leaves)/3 and leaves<=q; "
                "a star skeleton with all n-q-1 subdivisions on one arm attains the integer bound"
            ),
            "maximum_source_mechanism": (
                "Gentner-Henning-Rautenbach's exact fixed-degree-sequence forest maximum, "
                "specialized to a tree, is min(n-leaves,floor((n+leaves)/3)); "
                "optimize it over the feasible fixed-q leaf interval"
            ),
        },
        "burned_diagnostics": {
            "tree_count": 5447,
            "occupied_n_q_cells": 80,
            "all_cells_match_minimum_formula": True,
            "all_cells_match_maximum_formula": True,
            "all_cells_match_maximizing_leaf_optimizer": True,
            "cells": cells,
        },
        "representation_selection_matrix": [
            {
                "representation": "pairwise_linear_hull",
                "mathematical_object": "linear inequalities in domination_number, order, segment_count",
                "target": "domination_number",
                "conditioning_variables": ["order", "segment_count"],
                "feature_vocabulary": ["order", "segment_count"],
                "segment_count_only_new_invariant": True,
                "hidden_choices": "which projected facets to interpret",
                "structural_motivation": "weak",
                "fit_to_subdivision_mathematics": "poor; exact values are floor/ceiling piecewise envelopes",
                "interpretability": "moderate",
                "prior_art_risk": "high because the value envelope is already implied by stronger results",
                "exact_computation_feasibility": "high",
                "major_confounders": "would rediscover projections of an already-derived envelope",
                "single_axis_relative_to_prior": "possible feature substitution, but scientifically unnecessary",
                "decision": "REJECT",
                "reason": "linear hulls are not the natural form of the resolved value surface",
            },
            {
                "representation": "exact_conditioned_envelope",
                "mathematical_object": "exact min/max gamma conditioned on integer pair (n,q)",
                "target": "domination_number",
                "conditioning_variables": ["order", "segment_count"],
                "feature_vocabulary": ["order", "segment_count"],
                "segment_count_only_new_invariant": True,
                "hidden_choices": "none for values",
                "structural_motivation": "strong",
                "fit_to_subdivision_mathematics": "strong",
                "interpretability": "high",
                "prior_art_risk": "realized: both numeric extrema reduce to published stronger bounds",
                "exact_computation_feasibility": "high",
                "major_confounders": "none for diagnosis; fresh validation would add no scientific information",
                "single_axis_relative_to_prior": "not needed because no experiment is justified",
                "decision": "DEFER",
                "reason": "this is the natural mathematical representation, but the value problem is analytically resolved before fresh data",
            },
            {
                "representation": "residue_aware_envelope",
                "mathematical_object": "conditioned envelopes split by mod-3 data",
                "target": "domination_number",
                "conditioning_variables": ["order", "segment_count", "derived residues"],
                "feature_vocabulary": ["order", "segment_count"],
                "segment_count_only_new_invariant": True,
                "hidden_choices": "which residue coordinate to expose",
                "structural_motivation": "the floor/ceiling formulas encode mod-3 effects",
                "fit_to_subdivision_mathematics": "adequate but redundant",
                "interpretability": "moderate",
                "prior_art_risk": "high",
                "exact_computation_feasibility": "high",
                "major_confounders": "post-hoc residue splitting duplicates arithmetic already in the exact formulas",
                "single_axis_relative_to_prior": "would also change grammar/conditioning",
                "decision": "REJECT",
                "reason": "residues are consequences of the exact envelopes, not an independently needed coordinate",
            },
            {
                "representation": "structural_subdivision_recurrence",
                "mathematical_object": "domination under integer length assignments on a fixed reduced tree",
                "target": "domination_number",
                "conditioning_variables": ["reduced_tree", "segment_lengths"],
                "feature_vocabulary": ["segment_count", "structural length data"],
                "segment_count_only_new_invariant": False,
                "hidden_choices": "rooting/state formalism and equality-class parameterization",
                "structural_motivation": "strong for extremizer classification",
                "fit_to_subdivision_mathematics": "strong",
                "interpretability": "high once a canonical state theorem is chosen",
                "prior_art_risk": "subdivision-domination literature is substantial",
                "exact_computation_feasibility": "high",
                "major_confounders": "would add multiple structural axes before the residual classification question is isolated",
                "single_axis_relative_to_prior": "no",
                "decision": "DEFER",
                "reason": "promising only for the unresolved equality/classification residue, not ready as one controlled TreeForge axis",
            },
            {
                "representation": "maintain_experiment_pause",
                "mathematical_object": "no fresh-data experiment",
                "target": "none",
                "conditioning_variables": [],
                "feature_vocabulary": ["segment_count implemented for exact diagnostics only"],
                "segment_count_only_new_invariant": True,
                "hidden_choices": "none",
                "structural_motivation": "strong",
                "fit_to_subdivision_mathematics": "preserves the remaining equality question without forcing a grammar",
                "interpretability": "high",
                "prior_art_risk": "none created",
                "exact_computation_feasibility": "not applicable",
                "major_confounders": "none",
                "single_axis_relative_to_prior": "no scientific experiment is opened",
                "decision": "SELECT",
                "reason": "published stronger results settle the numeric extrema; complete fixed-(n,q) equality classes need mathematical triage before any experiment",
            },
        ],
        "decision": {
            "new_experiment_frozen": False,
            "experiment_id": None,
            "candidate_ids_allocated": [],
            "candidate_registry_changed": False,
            "experiment_registry_changed": False,
            "next_candidate_id": "TF-001158",
            "segment_count_implemented": True,
            "tf4_mis_fan_reopened": False,
            "tf7_tf9_theorem_thread_reopened": False,
            "order_15_consumed": False,
            "orders_at_least_15_untouched": True,
            "next_session_recommendation": (
                "Audit and, if useful, derive the complete equality classes for the two fixed-(n,q) "
                "envelopes from the located leaf/degree-sequence extremal literature before any fresh data."
            ),
        },
    }


def validate_repository_boundary() -> None:
    candidates = _jsonl(CANDIDATES)
    latest: dict[str, dict[str, object]] = {}
    for row in candidates:
        latest[str(row["candidate_id"])] = row
    expected = {
        "TF-001028": (7, "KNOWN_RESULT"),
        "TF-001034": (6, "ARTIFACT_OF_FEATURE_SET"),
        "TF-001037": (6, "ARTIFACT_OF_FEATURE_SET"),
        "TF-001091": (5, "ADVERSARIAL_PASSED"),
        "TF-001095": (5, "ADVERSARIAL_PASSED"),
    }
    for candidate_id, (revision, state) in expected.items():
        assert latest[candidate_id]["revision"] == revision
        assert latest[candidate_id]["lifecycle_state"] == state
    fan_states = Counter(str(latest[cid]["lifecycle_state"]) for cid in TF4_MIS_FAN)
    assert fan_states == Counter({"ADVERSARIAL_PASSED": 18, "ARTIFACT_OF_FEATURE_SET": 2})
    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"

    experiments = _jsonl(EXPERIMENTS)
    assert sum(row["experiment_id"] == "TF4-0001" for row in experiments) == 1
    assert all(
        not str(row["experiment_id"]).startswith(
            ("TF5", "TF6", "TF7", "TF8", "TF9", "TF10", "TF11", "TF12")
        )
        for row in experiments
    )
    assert not TF12_SPEC.exists()

    names = set(default_registry().names())
    assert "segment_count" in names


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
