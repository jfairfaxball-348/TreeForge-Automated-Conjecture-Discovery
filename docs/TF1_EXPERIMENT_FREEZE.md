# TF1-0001 experiment freeze

TF1-0001 was frozen before candidate generation. The parent repository state at freeze time was `f6c351b4a7a94941ab524bdfb9ec599409abcb2a`.

The measured cost profile supports discovery on all unlabeled trees of orders 2 through 10 (200 trees) and a completely untouched order-11 holdout (235 trees). Order 12 is deliberately excluded from the first controlled run: the current exhaustive maximal-independent-set counter grows sharply there, while the order-11 holdout is already larger than the discovery corpus.

The corpus computes the full exact core catalogue so that consistency checks and later interpretation can use it. TxGraffiti receives only the target `domination_number` and the seven frozen features `order`, `leaf_count`, `support_vertex_count`, `max_degree`, `diameter`, `matching_number`, and `maximal_independent_set_count`.

Calibration/redundant columns are not ordinary discovery features. In particular, `edge_count` and `degree_sum` are consistency columns, `min_degree` is constant on the nontrivial-tree universe, and `independence_number` is not supplied alongside `matching_number` because trees are bipartite and satisfy the standard relation `alpha(T)+nu(T)=|V(T)|`.

TxGraffiti remains pinned to package version `0.4.1` and upstream source revision `e37126da53b84150d142a5d61202b61f78521fcc`. TreeForge calls only its existing adapter using `convex_hull` and `ratios`, Morgan and Dalmatian acceptance heuristics, duplicate removal, and touch-count sorting. The explicit TxGraffiti hypothesis payload is empty because the dataframe itself is restricted to finite simple unlabeled trees; the mathematical hypotheses are recorded separately as `finite/simple/unlabeled/tree`.

Reserved hostile families are paths, stars, several spider regimes, structured caterpillars, balanced binary trees, double-stars, and brooms. They are not part of discovery data and are used only after holdout survival.

The machine-readable freeze is `experiments/TF1-0001/spec.json`. Any material change requires a new experiment ID.
