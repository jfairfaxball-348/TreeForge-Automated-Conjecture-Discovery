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

GitHub Actions run `36849930237` installed `txgraffiti==0.4.1` from PyPI and successfully exercised TreeForge's adapter through a real `ConjecturePlayground.discover(...)` call. No TxGraffiti API incompatibility was demonstrated in TF0.

The adapter is intentionally narrow: it wraps the documented `ConjecturePlayground` surface and does not yet expose `Graffiti3`, custom upstream conjecture object internals, or every generator/heuristic/post-processor. Those are scope choices, not known upstream defects. The only installation limitation encountered was the local execution sandbox's lack of PyPI network access; CI provided the live compatibility check.
