# Source lineage

TreeForge imports **concepts and research discipline**, not unstated theorems, from three predecessor repositories. They were inspected read-only at the following default-branch heads on 2026-10-01.

## TreeStack — Structural Certificates for Stacking on Trees

Repository: `jfairfaxball-348/TreeStack-Structural-Certificates-for-Stacking-on-Trees`  
Pinned `main`: `e1e437b8d02552b7c7ee0c4c74041b6ac956f063`

Legitimate import: TreeStack proves within that project an exact rooted branch-message criterion `StackableAt(T,C,r) iff S_r(C) > 0`, with a categorical empty-branch state distinct from integer message zero. It also defines the structural estimator

`estim(T) = max_r [1 + sum_{v=r or deg(v)>1} deg(v) 2^{dist(r,v)} + leaves_except_r]`

and proves the nontrivial-tree stacking-number formula using zero-score and arbitrary-defect structural certificates. Its Python implementation independently checks branch messages against legal-move reachability on bounded cases.

TreeForge use: an **optional** TreeStack-inspired module may compute the exact estimator and finite rooted-score-derived quantities. These are not default generic features and are not evidence for unrelated candidate statements.

Boundary: failed stronger local normalization statements recorded by TreeStack remain failures, not lemmas. TreeForge does not reinterpret bounded verification as proof beyond TreeStack's proved/formalised boundary.

## ProbStack — Random Stacking on Trees

Repository: `jfairfaxball-348/ProbStack-Random-Stacking-on-Trees`  
Pinned `main`: `ced67339f9289364a8c131bf2036af0502e2c08c`

Legitimate import: ProbStack studies uniform weak-composition configurations on deterministic trees, with `p_T(t)` the exact finite probability that a total-`t` configuration is stackable. It maintains independent legal-move and TreeStack-message evaluators. Its completed research programme is a fixed-offset asymptotic theorem for paths, with a deliberately narrower Lean/Palomar boundary.

TreeForge use: the finite quantity `p_T(t)` is mathematically meaningful as a **parameterised optional invariant** on general trees. It may be computed exactly for conservative `(n,t)` ranges and can motivate later comparisons.

Boundary: the completed path programme is not reopened here. TreeForge does not import a zero-offset law, finite-`n` monotonicity, a Poisson front law, or an arbitrary-tree asymptotic extension; ProbStack explicitly does not claim them.

## Greedy Uniformity on Trees

Repository: `jfairfaxball-348/Greedy-Uniformity-on-Trees`  
Pinned `main`: `2fb997397daa8c16b80dd1f4aef9a91303c67eb6`

Legitimate import: the project studies the random-permutation greedy maximal-independent-set law `G_T`, the uniform law on maximal independent sets `U_T`, and total-variation bias `b(T)`. Its frozen theorem package proves/formalises that exact uniformity occurs only for `K_1` and `K_2`, and gives an explicit near-uniform mixed-spider family. Exact computations through order 11 are evidence supporting the research process, not an extremal theorem.

TreeForge use: maximal-independent-set counts and, on conservative orders, exact greedy output-law/bias quantities are **optional** interpretable invariants.

Boundary: the all-order extremal problem `a_n = min_{|V(T)|=n} b(T)`, sharp bounds, and minimiser structure remain outside the frozen theorem package and are not imported as facts.

## General rule

A numerical table, conjecture note, unfinished direction, or negative prior-art search in a predecessor repository is not promoted to theorem status in TreeForge. Any imported mathematical definition is re-documented with a pin and tested independently where feasible.
