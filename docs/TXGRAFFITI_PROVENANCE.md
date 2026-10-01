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
