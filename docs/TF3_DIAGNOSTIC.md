# TF3 interpretability diagnosis

TF3-DIAG-0001 uses only already-exposed TF2 discovery output and discovery rows for candidate-generation comparisons. It does not reinterpret TF2-0001, allocate candidate IDs, or use order-12 survival to select a coefficient, statement, or threshold.

## Verified TF2 geometry

The 998 final TF2 statements are overwhelmingly dense:

| distinct RHS discovery features | final statements | order-12 survivors |
|---:|---:|---:|
| 1 | 8 | 3 |
| 2 | 4 | 0 |
| 3 | 7 | 1 |
| 4 | 12 | 3 |
| 5 | 61 | 7 |
| 6 | 217 | 31 |
| 7 | 689 | 29 |

Thus 979/998 (98.1%) final statements use at least four RHS features, and 689/998 (69.0%) use all seven. Among the 74 already-consumed order-12 survivors, 70/74 (94.6%) still use at least four features. The 998 statements split into 190 upper bounds and 808 lower bounds.

Discovery touch counts range from 1 to 149, with median 10 and 90th percentile 17. The largest rational denominator appearing in an individual candidate has median 10, 90th percentile 60, and maximum 1208. These facts reinforce, but do not replace, the main geometric diagnosis: most final output consists of high-dimensional facets involving many supplied features.

The committed final metadata does not preserve a direct generator-source label for each statement. Therefore TF3 does not retroactively guess whether a final statement came from `convex_hull` or `ratios`; it isolates methods in diagnostic reruns on the already-exposed discovery corpus.

## Why TF2 remained large

TF2's discovery-only performance probe already showed 42,068 full-dimensional Qhull facets. Under the normalized always-true hypothesis, Morgan cannot remove statements on hypothesis-generality grounds. Dalmatian reduced the frozen stream to 10,753 and exact duplicate removal reduced it to 998, but exact syntactic relation equality is much weaker than mathematical family equivalence. The result was a large collection of dense rational facets, many with no evident structural mechanism.

This is primarily a full-dimensional convex-hull / seven-feature interaction problem. Low touch counts, rationalized Qhull coefficients, and only-exact duplicate equivalence contribute additional opacity, but they do not explain away the concentration of 6- and 7-feature statements.

## Predeclared alternatives benchmarked

Corrected diagnostic validation: GitHub Actions run `36907058956`.

| option | discovery-side result | interpretation |
|---|---|---|
| A. ratios only | 14 raw; 12 after Dalmatian; 12 final; all 12 use exactly one RHS feature; max denominator 13; ~0.342 s | Removes the diagnosed hull geometry while keeping target, features, heuristics, post-processors, and hypothesis semantics fixed. |
| C. unchanged full generation + RHS-support <= 2 gate | same 23,268 raw / 10,753 after Dalmatian / 998 deduplicated TF2 stream; 12 would pass the diagnostic gate | Produces a small admitted set only after paying for and creating the full opaque stream, and adds a new threshold/filter axis. |
| D. 21 fixed pairwise convex hulls | 259 raw; 214 after Dalmatian; 205 post-duplicate across runs; 146 after cross-run exact dedup; 127 use two RHS features; max denominator 61; ~0.778 s | More interpretable than TF2, but still an order of magnitude larger than ratios-only and introduces a multi-run hull design. |

No order-12 survival information was used to choose among these alternatives.

## TF3 choice

TF3-0001 changes exactly one discovery axis: the TxGraffiti method set is restricted from
`[convex_hull, ratios]` to `[ratios]`.

There is no post-generation touch-count threshold, coefficient threshold, denominator threshold, candidate cap, or manually selected shortlist. A final ratios-only statement is expected to contain exactly one distinct RHS discovery feature. If the pinned upstream behavior violates that expected grammar, the scientific run aborts rather than silently filtering the statement.

The target remains `domination_number`; the seven discovery features, discovery orders 2-10, Morgan/Dalmatian heuristics, duplicate removal, touch-count sorting, and empty-hypothesis-to-`None` semantics remain unchanged.

## Fresh order-13 feasibility

A timing-only pre-freeze probe generated all 1,301 unlabeled order-13 trees and timed the two known expensive exact invariants. On GitHub Actions run `36907058956`, tree generation took about 0.187 s, domination number about 0.949 s, and maximal-independent-set counting about 23.976 s.

The probe did not persist, print, inspect, rank, or compare individual order-13 invariant values. No TF3 candidate batch existed. Its sole purpose was runtime feasibility. TF3 therefore freezes all order-13 unlabeled trees as its fresh exhaustive holdout, constructed by the scientific runner only after the discovery-side candidate batch has been frozen.

## Diagnostic failures preserved

Run `36906556561` failed before the diagnostic because a new method-selection unit test compared object identity across two separately constructed fake module fixtures. Run `36906621879` then completed but exposed over-escaped regular expressions in the diagnostic-only complexity parser. The first attempted parser correction, run `36907013799`, failed its new parser unit test and prevented the diagnostic step from running. These were implementation/diagnostic failures only: no TF3 scientific generation, permanent candidate IDs, or fresh validation comparisons occurred. The corrected unchanged diagnostic passed in run `36907058956`.
