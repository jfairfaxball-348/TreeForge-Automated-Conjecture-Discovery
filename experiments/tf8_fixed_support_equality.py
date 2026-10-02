#!/usr/bin/env python3
"""Reproduce the TF8 equality characterization for the fixed-support MIS theorem."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path

import networkx as nx

from experiments.tf7_support_mis_diagnosis import fibonacci, independent_set_count_forest
from treeforge.invariants.core import maximal_independent_set_count, support_vertex_count
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import canonical_tree_identity, generate_unlabeled_trees

STARTING_MAIN = "cdfa0cdd86aee25498c7315dfcb083cfb1c5a7c1"
STARTING_MAIN_CI = 37050985352
OUTPUT = Path("experiments/TF8-DIAG-0001/diagnosis.json")
CANDIDATE_REGISTRY = Path("data/registry/candidates.jsonl")
EXPERIMENT_REGISTRY = Path("data/registry/experiments.jsonl")

TF4_MIS_FAN = (
    "TF-001033",
    "TF-001034",
    "TF-001037",
    "TF-001090",
    "TF-001091",
    "TF-001093",
    "TF-001095",
    "TF-001098",
    "TF-001099",
    "TF-001134",
    "TF-001135",
    "TF-001137",
    "TF-001139",
    "TF-001140",
    "TF-001141",
    "TF-001142",
    "TF-001144",
    "TF-001145",
    "TF-001154",
    "TF-001155",
)


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def leaf_vertices(graph: nx.Graph) -> set[int]:
    return {vertex for vertex, degree in graph.degree() if degree == 1}


def support_vertices(graph: nx.Graph) -> set[int]:
    leaves = leaf_vertices(graph)
    return {
        vertex
        for vertex in graph
        if any(neighbor in leaves for neighbor in graph.neighbors(vertex))
    }


def support_induced_forest(graph: nx.Graph) -> nx.Graph:
    return graph.subgraph(support_vertices(graph)).copy()


def core_vertices(graph: nx.Graph) -> set[int]:
    """Vertices that are neither supports nor leaves."""
    return set(graph) - support_vertices(graph) - leaf_vertices(graph)


def core_is_independent(graph: nx.Graph) -> bool:
    return graph.subgraph(core_vertices(graph)).number_of_edges() == 0


def forest_is_path(forest: nx.Graph) -> bool:
    """Recognize P_s, taking the empty forest as P_0."""
    order = forest.number_of_nodes()
    if order == 0:
        return True
    if not nx.is_tree(forest):
        return False
    return max(dict(forest.degree()).values(), default=0) <= 2


def is_path_leaf_blowup(graph: nx.Graph) -> bool:
    """Recognize a path whose vertices each carry one or more private leaves."""
    supports = support_vertices(graph)
    leaves = leaf_vertices(graph)
    if not supports or supports & leaves:
        return False
    if set(graph) != supports | leaves:
        return False
    return forest_is_path(graph.subgraph(supports).copy())


def _positive_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts < 1 or total < parts:
        return
    if parts == 1:
        yield (total,)
        return
    for first in range(1, total - parts + 2):
        for rest in _positive_compositions(total - first, parts - 1):
            yield (first, *rest)


def _path_leaf_blowup(support_count: int, multiplicities: tuple[int, ...]) -> nx.Graph:
    if support_count < 1 or len(multiplicities) != support_count:
        raise ValueError("multiplicities must match a positive support path")
    if any(value < 1 for value in multiplicities):
        raise ValueError("every support must receive at least one leaf")

    graph = nx.path_graph(support_count)
    nxt = support_count
    for support, count in enumerate(multiplicities):
        for _ in range(count):
            graph.add_edge(support, nxt)
            nxt += 1
    return graph


def _expected_leaf_blowup_identities(
    support_count: int, order: int
) -> set[tuple[int, str]]:
    leaf_total = order - support_count
    return {
        canonical_tree_identity(_path_leaf_blowup(support_count, multiplicities))
        for multiplicities in _positive_compositions(leaf_total, support_count)
    }


def _path_probe(order: int) -> dict[str, object]:
    graph = nx.path_graph(order)
    forest = support_induced_forest(graph)
    return {
        "order": order,
        "support_vertex_count": support_vertex_count(graph),
        "core_vertex_count": len(core_vertices(graph)),
        "core_edge_count": graph.subgraph(core_vertices(graph)).number_of_edges(),
        "maximal_independent_set_count": maximal_independent_set_count(graph),
        "support_forest_independent_set_count": independent_set_count_forest(forest),
    }


def _exposed_analysis() -> dict[str, object]:
    trees = generate_unlabeled_trees(1, 14)
    if len(trees) != 5447:
        raise AssertionError("exposed orders 1-14 corpus changed")

    injection_equivalence_failures = 0
    forest_equality_failures = 0
    fixed_support_characterization_failures = 0
    injection_equalities = 0
    equality_identities: defaultdict[tuple[int, int], set[tuple[int, str]]] = defaultdict(set)

    for graph in trees:
        order = graph.number_of_nodes()
        support_count = support_vertex_count(graph)
        forest = support_induced_forest(graph)
        support_independent_sets = independent_set_count_forest(forest)
        maximal_independent_sets = maximal_independent_set_count(graph)

        if order != 2:
            injection_equality = maximal_independent_sets == support_independent_sets
            if injection_equality:
                injection_equalities += 1
            if injection_equality != core_is_independent(graph):
                injection_equivalence_failures += 1

        forest_equality = support_independent_sets == fibonacci(support_count + 2)
        if forest_equality != forest_is_path(forest):
            forest_equality_failures += 1

        if support_count >= 3:
            extremal_equality = maximal_independent_sets == fibonacci(support_count + 2)
            structural_equality = is_path_leaf_blowup(graph)
            if extremal_equality != structural_equality:
                fixed_support_characterization_failures += 1
            if extremal_equality:
                equality_identities[(support_count, order)].add(canonical_tree_identity(graph))

    if any(
        (
            injection_equivalence_failures,
            forest_equality_failures,
            fixed_support_characterization_failures,
        )
    ):
        raise AssertionError("TF8 exposed equality characterization check failed")

    family_counts: dict[str, dict[str, int]] = {}
    generated_family_match_failures = 0
    for support_count in range(3, 8):
        per_order: dict[str, int] = {}
        for order in range(2 * support_count, 15):
            expected = _expected_leaf_blowup_identities(support_count, order)
            actual = equality_identities[(support_count, order)]
            if expected != actual:
                generated_family_match_failures += 1
            if actual:
                per_order[str(order)] = len(actual)
        family_counts[str(support_count)] = per_order

    if generated_family_match_failures:
        raise AssertionError("exposed extremizers differ from the path leaf-blowup family")

    return {
        "orders": [1, 14],
        "tree_count": len(trees),
        "classification": "burned/exposed interpretation data only; not proof",
        "injection_equality_equivalence_failures_excluding_P2": injection_equivalence_failures,
        "injection_equality_tree_count_excluding_P2": injection_equalities,
        "support_forest_path_equality_failures": forest_equality_failures,
        "fixed_support_characterization_failures_for_s_at_least_3": (
            fixed_support_characterization_failures
        ),
        "generated_leaf_blowup_family_match_failures": generated_family_match_failures,
        "fixed_support_equality_counts_by_s_and_order": family_counts,
        "internal_core_examples": {
            "P5": _path_probe(5),
            "P6": _path_probe(6),
            "interpretation": (
                "P5 has one core vertex and equality m=i(T[S]); P6 has a core edge and strict "
                "inequality. Internal vertices alone do not break equality; adjacency inside the "
                "core does."
            ),
        },
    }


def _provenance_verification() -> dict[str, object]:
    candidates = _jsonl(CANDIDATE_REGISTRY)
    latest: dict[str, dict[str, object]] = {}
    for row in candidates:
        latest[str(row["candidate_id"])] = row

    expected_states = {
        "TF-001028": (7, "KNOWN_RESULT"),
        "TF-001034": (6, "ARTIFACT_OF_FEATURE_SET"),
        "TF-001037": (6, "ARTIFACT_OF_FEATURE_SET"),
        "TF-001091": (5, "ADVERSARIAL_PASSED"),
        "TF-001095": (5, "ADVERSARIAL_PASSED"),
    }
    for candidate_id, (revision, state) in expected_states.items():
        row = latest.get(candidate_id)
        if row is None or row["revision"] != revision or row["lifecycle_state"] != state:
            raise AssertionError(f"unexpected lifecycle state for {candidate_id}")

    residual_states = {
        candidate_id: str(latest[candidate_id]["lifecycle_state"])
        for candidate_id in TF4_MIS_FAN
    }
    if sum(state == "ADVERSARIAL_PASSED" for state in residual_states.values()) != 18:
        raise AssertionError("TF4 MIS fan no longer has exactly 18 finite survivors")
    if sum(state == "ARTIFACT_OF_FEATURE_SET" for state in residual_states.values()) != 2:
        raise AssertionError("TF4 MIS fan no longer has exactly two projection artifacts")

    next_id = CandidateRegistry(CANDIDATE_REGISTRY).next_id()
    if next_id != "TF-001158":
        raise AssertionError("candidate-ID continuity changed")

    experiments = _jsonl(EXPERIMENT_REGISTRY)
    if sum(row["experiment_id"] == "TF4-0001" for row in experiments) != 1:
        raise AssertionError("TF4-0001 registry multiplicity changed")
    later_experiments = [
        str(row["experiment_id"])
        for row in experiments
        if str(row["experiment_id"]).startswith(("TF5", "TF6", "TF7", "TF8"))
    ]
    if later_experiments:
        raise AssertionError("unexpected TF5-TF8 scientific experiment registry record")

    return {
        "starting_main_head": STARTING_MAIN,
        "starting_main_ci_run": STARTING_MAIN_CI,
        "tf7_pr": 13,
        "tf001028": {"revision": 7, "state": "KNOWN_RESULT"},
        "tf001034": {"revision": 6, "state": "ARTIFACT_OF_FEATURE_SET"},
        "tf001037": {"revision": 6, "state": "ARTIFACT_OF_FEATURE_SET"},
        "tf001091": {"revision": 5, "state": "ADVERSARIAL_PASSED"},
        "tf001095": {"revision": 5, "state": "ADVERSARIAL_PASSED"},
        "tf4_mis_fan": {
            "adversarial_passed": 18,
            "artifact_of_feature_set": 2,
            "candidate_ids": list(TF4_MIS_FAN),
        },
        "highest_allocated_candidate": "TF-001157",
        "next_permanent_candidate_id": next_id,
        "tf4_experiment_registry_records": 1,
        "tf5_tf6_tf7_tf8_scientific_experiment_records": 0,
    }


def build_diagnosis() -> dict[str, object]:
    return {
        "analysis_id": "TF8-DIAG-0001",
        "classification": "STRUCTURAL_EQUALITY_CHARACTERIZATION_NO_SCIENTIFIC_EXPERIMENT",
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, 14],
            "orders_at_least_15": "untouched",
            "tf2_tf3_tf4_hostile_sets": "burned",
            "tf5_family_instances": "burned interpretation data",
        },
        "provenance_verification": _provenance_verification(),
        "structural_result": {
            "notation": (
                "m(T)=maximal independent set count; S(T)=support vertices; L(T)=leaves; "
                "C(T)=V(T) minus (S(T) union L(T)); i(F)=all independent sets of a forest F."
            ),
            "forest_equality": (
                "For every forest F on s vertices, i(F)=F_(s+2) iff F is the path P_s, "
                "with P_0 interpreted as the empty forest."
            ),
            "support_injection_equality": (
                "For every finite tree T other than P2, m(T)=i(T[S(T)]) iff the induced core "
                "T[C(T)] is edgeless. Equivalently every component of the non-support/non-leaf "
                "core is a single vertex."
            ),
            "support_injection_mechanism": (
                "Maximal independent sets partition by I=M intersect S(T). Once I is fixed, leaf "
                "membership is forced. For I empty, completions are exactly maximal independent "
                "sets of T[C(T)], so any core edge gives at least two completions. If the core is "
                "edgeless, each core vertex is forced in exactly when it has no neighbor in I, "
                "giving one completion for every independent I subset S(T)."
            ),
            "fixed_support_equality_for_s_at_least_3": (
                "m(T)=F_(s(T)+2) iff T is obtained from P_s by attaching at least one private "
                "leaf to every path vertex and adding no other vertices."
            ),
            "twin_reduced_form": (
                "After deleting duplicate leaves while retaining one leaf at each support, every "
                "s>=3 equality tree reduces to exactly P_s corona K1. Conversely arbitrary "
                "duplicate-leaf additions at those supports preserve m and s and remain equality "
                "trees."
            ),
            "why_no_other_core_survives_extremality": (
                "Forest equality forces T[S(T)]=P_s, hence the support-induced subgraph is "
                "connected. In a tree, any nonempty core vertex together with an edgeless core "
                "would have at least two support neighbors, creating a cycle through the connected "
                "support path. Therefore the core is empty."
            ),
            "small_support_cases": {
                "s=0": "K1 is the unique tree and has m=1.",
                "s=1": "The equality trees are exactly stars K_(1,k) with k>=2; all have m=2.",
                "s=2": (
                    "The global fixed-support minimum is the exceptional P2 with m=2. Among "
                    "T!=P2, the Fibonacci-chain equality m=3 occurs exactly for a support edge "
                    "with at least one private leaf attached to each endpoint."
                ),
            },
        },
        "exposed_computational_check": _exposed_analysis(),
        "candidate_consequences": {
            "lifecycle_revisions": [],
            "remaining_mis_survivors": 18,
            "reason": (
                "The equality theorem characterizes the sharp lower envelope of MIS at fixed "
                "support count but does not prove or refute any of the 18 surviving domination "
                "facets. Their coefficients are not reopened or mined."
            ),
        },
        "coordinate_decision": {
            "raw_maximal_independent_set_count": "RETAIN_UNCHANGED",
            "support_forest_independent_set_count": "STRUCTURALLY_CANONICAL_LOWER_ENVELOPE_ONLY",
            "duplicate_leaf_reduction": "STRUCTURAL_QUOTIENT_NOT_NEW_DISCOVERY_COORDINATE",
            "reason": (
                "i(T[S]) is canonical in the proof but intentionally discards core-completion "
                "multiplicity, while twin-leaf reduction preserves m and s but changes other "
                "discovery coordinates. Neither supplies an independent reason that domination "
                "should be linear in a replacement feature."
            ),
        },
        "decision": {
            "new_experiment_frozen": False,
            "candidate_ids_allocated": [],
            "experiment_registry_updated": False,
            "raw_mis_coordinate_changed": False,
            "tf4_mis_fan_reopened": False,
            "theorem_repository_created": False,
            "reason": (
                "The fixed-support extremal problem is structurally complete: the only minimizers "
                "for s>=3 are duplicate-leaf blowups of path coronas. This is meaningful theorem "
                "content but does not independently select a new TreeForge discovery axis."
            ),
            "next_session_recommendation": (
                "Keep orders >=15 untouched and the 18 TF4 MIS survivors archived. If the equality "
                "theorem is pursued further, the next defensible session is a bounded prior-art "
                "audit of this fixed-support/equality result before any theorem-repository decision, "
                "not a new discovery experiment."
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
