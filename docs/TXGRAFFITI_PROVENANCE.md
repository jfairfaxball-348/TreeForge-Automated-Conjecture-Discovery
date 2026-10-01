# TxGraffiti provenance and adapter boundary

Upstream repository: `RandyRDavila/TxGraffiti2`  
Inspected default branch: `main`  
Pinned source revision: `e37126da53b84150d142a5d61202b61f78521fcc`  
Pinned package version: `txgraffiti==0.4.1`  
Upstream Python requirement: `>=3.8`

The inspected README documents the stable-style interface
`txgraffiti.playground.ConjecturePlayground`, generator functions including `convex_hull` and `ratios`, heuristics including Morgan/Dalmatian filters, and post-processors such as duplicate removal and touch-count sorting. The same revision also contains a newer `Graffiti3` interface for nonlinear/sufficient-condition conjecturing.

TreeForge initially wraps only the smaller `ConjecturePlayground.discover(...)` surface. All upstream imports live in `treeforge.conjecturing.txgraffiti_adapter`. TreeForge does not fork or modify TxGraffiti.

The adapter deliberately returns plain TreeForge `GeneratedStatement` records rather than exposing upstream conjecture objects. This keeps registry/provenance logic independent of TxGraffiti API evolution.

## TF0 compatibility result

GitHub Actions run `36849930237` installed `txgraffiti==0.4.1` from PyPI and successfully exercised TreeForge's adapter through a real `ConjecturePlayground.discover(...)` call.

## TF1 compatibility and controlled-run result

GitHub Actions run `36852665881`, at TreeForge source commit `e5175b5f5667195adf64ccae75e3dc42f0061086`, again installed and live-tested `txgraffiti==0.4.1` before executing frozen experiment `TF1-0001`. The adapter completed without an API incompatibility and returned zero candidate statements for the frozen domination-number target and feature/configuration set.

Zero output is an experiment result, not evidence of an adapter defect and not evidence that no mathematical relation exists.

The adapter remains intentionally narrow: it wraps the documented `ConjecturePlayground` surface and does not expose `Graffiti3`, custom upstream conjecture internals, or every generator/heuristic/post-processor.


## TF2 hypothesis-semantics diagnosis

`TF2-DIAG-0001`, live-validated in GitHub Actions run `36855637323`, established why the frozen TF1 adapter call emitted no statements. In pinned TxGraffiti `0.4.1`, `ConjecturePlayground.generate` treats `hypothesis=None` as the always-true base predicate, while an explicit empty list iterates over no hypotheses and invokes no generators. TreeForge had intended its empty payload to mean “no additional predicate beyond the finite-simple-tree universe.”

TreeForge therefore normalizes an empty hypothesis payload to upstream `None` inside the adapter. This is classified as a TreeForge/TxGraffiti adapter/configuration semantic mismatch. It is not described as an upstream TxGraffiti bug, and it does not rewrite the frozen TF1 result.

## TF2 live controlled-run result

The unchanged frozen TF2 mathematical configuration was executed successfully at TreeForge scientific source commit `d091d88889fa72322bfc49a5531bc30b1f31b049` in GitHub Actions run `36888114138`.

The first live attempt, run `36875119955`, exposed a severe performance bottleneck and was provisionally closed before a scientific artifact was available for inspection. It later completed and uploaded an artifact; an append-only audit found its mathematical output equivalent to the repaired authoritative run after removing source-commit provenance labels. A discovery-only probe in run `36887027180` showed that the 8-dimensional convex hull contained 42,068 facets while Qhull itself completed in about 0.48 seconds. The costly path was repeated upstream-style state reconstruction while applying Morgan/Dalmatian to the large always-true facet stream.

TreeForge added a narrowly scoped execution optimization for the normalized always-true case without changing the frozen heuristics: Morgan is an exact no-op when every generated conjecture has the identical hypothesis mask, and Dalmatian's pointwise minimum of prior accepted upper bounds is cached incrementally instead of recomputed by repeated concatenation. A live pinned-package test compares the complete ordered output of this path with the unoptimized upstream pipeline on a nondegenerate dataset. Clean repaired preflight run `36887887082` passed before the successful scientific execution.

The successful run recorded 23,268 raw generator outputs, 10,753 survivors after Dalmatian, and 998 final statements after duplicate removal and touch-count sorting. These counts and the complete structured raw statements are preserved under `experiments/TF2-0001/`.

The adapter remains intentionally narrow. TreeForge has not switched TF2 to `Graffiti3`, changed the frozen generator set, or modified TxGraffiti upstream.
