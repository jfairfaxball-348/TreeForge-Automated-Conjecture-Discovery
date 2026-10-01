"""Optional TreeStack-derived structural invariants.

Definition provenance: TreeStack commit e1e437b8d02552b7c7ee0c4c74041b6ac956f063.
"""

from __future__ import annotations

import networkx as nx


def treestack_estimate(graph: nx.Graph) -> int:
    """Compute TreeStack's exact estimator on a finite tree."""
    if not nx.is_tree(graph) or graph.number_of_nodes() < 1:
        raise ValueError("expected a nonempty tree")
    distances = dict(nx.all_pairs_shortest_path_length(graph))

    def root_estimate(root: int) -> int:
        sigma = 1 + sum(
            graph.degree(v) * 2 ** distances[root][v]
            for v in graph.nodes()
            if v == root or graph.degree(v) > 1
        )
        leaves_except_root = sum(v != root and graph.degree(v) == 1 for v in graph.nodes())
        return sigma + leaves_except_root

    return max(root_estimate(root) for root in graph.nodes())
