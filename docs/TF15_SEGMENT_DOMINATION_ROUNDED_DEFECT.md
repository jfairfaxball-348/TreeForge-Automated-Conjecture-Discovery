# TF15 — strict-rounded domination defect classification

Date: 2026-10-03

TF15 attacks only the strict-rounded residue-1/2 realization problem isolated by TF14. It remains
a theorem/equality-classification session. No TxGraffiti discovery run is performed, no candidate
ID is allocated, no new default invariant is added, and every finite diagnostic remains restricted
to the 5,447 already burned unlabeled trees of orders 1--14.

## Verified starting state

TF15 starts from exact main commit
`63fa16c17f04b27b541a3222b10f6c933165aa39`, the TF14 merge commit for PR #20.

The verified TF14 provenance is:

- PR #20 merged;
- exact PR head `4afc22d70df65be24057605ccf164fbfd66b23b8`;
- exact PR-head Actions run `37132239373`, successful;
- merge commit / starting main
  `63fa16c17f04b27b541a3222b10f6c933165aa39`;
- post-merge Actions run `37132400796`, successful.

Both green runs passed installation, all unit tests, byte-compilation, Ruff, deterministic
calibration, live pinned `txgraffiti==0.4.1` compatibility, historical registry/result checks, and
the explicit TF6 through TF14 deterministic diagnoses.

The earlier TF14 PR-head run `37132064937` remains an append-only non-scientific failure: it passed
installation, all unit tests, and compileall before Ruff found two unused imports in the new TF14
test module. Their removal did not change mathematics or data.

At TF15 entry, `segment_count` is still the exact invariant `q=n-n_2-1`, the candidate registry
still ends at TF-001157, TF-001158 is still next, and the experiment registry still contains no
scientific record after TF4-0001. There is no TF14-0001 or TF15-0001 scientific experiment.
Orders at least 15 remain untouched.

## Exact problem inherited from TF14

For an optimizing fixed-(n,q) leaf count L, put

`A=n-L` and `B=floor((n+L)/3)`.

TF14 completely resolved `A<=B`: a realization is maximum exactly when every nonleaf is a support.
On the only remaining branch, `B<A`, Favaron's independent-domination bound gives the exact
realization-level reduction

`gamma(T)=B iff gamma(T)=i(T)=B`.

If `n+L` is divisible by 3, this is already the intersection of Favaron's published real-equality
trees with the published `(gamma,i)`-tree class.

Thus TF15 starts with only:

> among `(gamma,i)`-trees, characterize those with
> `i(T)=floor((n+L)/3)` when `n+L` is 1 or 2 modulo 3.

Define the Favaron numerator defect

`epsilon(T)=n(T)+L(T)-3i(T)`.

The two unresolved cases are exactly `epsilon=1` and `epsilon=2`.

## Published `(gamma,i)` grammar reconstructed

The exact constructive source used by TF15 is:

Michael Dorfling, Wayne Goddard, Michael A. Henning and C. M. Mynhardt,
“Construction of trees and graphs with equal domination parameters”,
*Discrete Mathematics* 306 (2006), 2647--2654,
DOI `10.1016/j.disc.2006.04.031`.

The paper works first with packing number `rho`. For trees, its Fact 1 records the classical identity
`gamma=rho`. A `rho-i` labeling partitions the vertices into statuses A, B, C and D so that

- `S_A union S_D` is an independent dominating set;
- `S_C union S_D` is a packing;
- `|S_A|=|S_C|`.

Consequently both displayed sets have the common optimum size `rho=i`; on a tree this is also
`gamma=i`.

The class `L` starts from either a single D-labeled vertex `P1` or an A--C labeled `P2` and is
closed under six operations. If `y` is the existing attacher, the operations are:

| operation | allowed status of `y` | attached labeled tree |
|---|---|---|
| T1 | A or D | add `x` adjacent to `y`, with `x:B` |
| T2 | A or B | attach path `x-w`, with `x:B`, `w:D` |
| T3 | B | attach path `x-w`, with `x:A`, `w:C` |
| T4 | B or C | attach path `x-w-z`, with `x:B`, `w:A`, `z:C` |
| T5 | A | attach path `x-w-z`, with `x:B`, `w:C`, `z:A` |
| T6 | B | attach path `v-u-x-w-z` at its internal vertex `x` to `y`, with `x:B`, `w,v:C`, `z,u:A` |

Their Theorem 7 says that a labeled tree is a `rho-i` tree iff it lies in this class.
Corollary 9 then says that the unlabeled `(gamma,i)`-trees are exactly the trees admitting such a
labeling. Most importantly for a canonical base calculation, Observation 11 says that every
`rho-i` tree has *some* valid labeling and construction starting from the D-labeled `P1`.

The earlier paper

E. J. Cockayne, O. Favaron, C. M. Mynhardt and J. Puech,
“A characterization of `(gamma,i)`-trees”,
*Journal of Graph Theory* 34 (2000), 277--292,

gives another exact characterization in terms of the sets of vertices contained in all minimum
dominating and minimum independent dominating sets. The accessible bounded sources confirm that
set-based theorem but did not expose enough full theorem text to reconstruct those “in every
minimum set” classes without guessing. TF15 therefore does **not** assign such semantics to the
2006 A/B/C/D statuses: those statuses encode chosen optimum sets in a valid labeling, not
membership in every optimum set. The fully accessible 2006 constructive theorem is sufficient for
the defect argument.

## Defect recurrence through the six operations

The constructive grammar gives an exact local recurrence for

`epsilon=n+L-3i`.

For a valid labeled construction, the increase in `i` is read directly from the new A/D vertices:

- T1: `Delta i=0`;
- T2, T3, T4, T5: `Delta i=1`;
- T6: `Delta i=2`.

The number of newly created leaf endpoints is one for T1--T5 and two for T6. If the existing
attacher `y` is already a leaf, it ceases to be a leaf after the attachment; otherwise no old leaf
is lost. Therefore, after the initial step, the defect changes exactly as follows:

| operation | leaf attacher | nonleaf attacher |
|---|---:|---:|
| T1 | +1 | +2 |
| T2 | -1 | 0 |
| T3 | -1 | 0 |
| T4 | 0 | +1 |
| T5 | 0 | +1 |
| T6 | 0 | +1 |

There is one base exception because the starting vertex of `P1` is isolated rather than a leaf.
For the D-labeled `P1`,

`(n,L,i)=(1,0,1)` and `epsilon=-2`.

Observation 11 lets every nontrivial `(gamma,i)`-tree start there. The mandatory first T1 turns
that `P1` into a D--B `P2`; both vertices are then leaves, so

`(n,L,i)=(2,2,1)` and `epsilon=1`.

Thus every nontrivial published construction may be viewed as a defect walk starting at 1 after
its first T1 and then using the table above.

This recurrence is exact, not empirical. The operations preserve a `rho-i` labeling, so their
`Delta i` values are exact. Their attached paths make the leaf changes explicit. Since every
nontrivial `(gamma,i)`-tree has a P1-starting construction, the converse direction is also covered.

The construction is not unique, but that causes no ambiguity: summing the local increments along
*any* valid construction gives the graph invariant `n+L-3i` at the endpoint. Observation 11 is
needed only to give every tree the same convenient starting defect.

## Complete residue-1/2 theorem

### Theorem — constructive Favaron-defect classification

Let T be a nontrivial tree satisfying `gamma(T)=i(T)`. Choose any Dorfling--Goddard--Henning--
Mynhardt valid P1-starting construction supplied by Observation 11, discard its mandatory first T1,
and start a defect counter at 1. For every later operation, update the counter by the preceding
table according to the operation and whether its attacher was a leaf immediately before attachment.

Then the final counter is exactly

`epsilon(T)=n(T)+L(T)-3i(T)`.

In particular:

- `i(T)=floor((n+L)/3)` with `n+L == 1 (mod 3)` iff the defect walk ends at 1;
- `i(T)=floor((n+L)/3)` with `n+L == 2 (mod 3)` iff the defect walk ends at 2.

Because each intermediate nontrivial tree is again a `(gamma,i)`-tree, Favaron's inequality also
shows that every intermediate defect is nonnegative.

**Proof.** The base after the first T1 has defect 1. The six local changes are exactly the
arithmetic in the preceding table, so induction over the construction gives the endpoint identity.
For the converse, Dorfling et al. Corollary 9 and Observation 11 provide such a construction for
every `(gamma,i)`-tree. Finally `epsilon` is congruent to `n+L` modulo 3; endpoint 1 or 2 is
therefore exactly integer saturation of Favaron's bound in the corresponding residue. QED.

Status for residue 1:
**TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS**.

Status for residue 2:
**TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS**.

This is a complete recursive structural characterization. It is not claimed to be a unique,
construction-independent geometric normal form.

## Favaron proof and near-equality audit

Odile Favaron,
“A bound on the independent domination number of a tree”,
*Vishwa International Journal of Graph Theory* 1 (1992), 19--27,
proves

`i(T) <= (n+L)/3`

and gives the full list of real-equality trees.

The original 1992 full text was not exposed by the bounded sources available to TF15. Two later
sources explicitly confirm the scope of Favaron's result:

- Goddard--Henning (2013), *Independent domination in graphs: A survey and recent results*,
  Theorem 2.14, records the bound and says Favaron's proof supplies the full extremal list;
- Bujtás--Iršič Chenoweth--Klavžar--Zhang (2026),
  *Discrete Mathematics* 349, 114972, again states that Favaron gave the full extremal list and
  extends the leaf bound to d-distance independent domination for `d>=2`.

The TF15 search also checked the 2025 domination/independent-domination literature and direct
queries for near equality, integer equality after flooring, `3i=n+L-1`, `3i=n+L-2`, stability,
prescribed leaves, and `(gamma,i)` trees with leaf bounds. No published defect-1/2 list was located.
This is a bounded negative search, not evidence that such a result is absent from the literature or
that the bookkeeping theorem above is novel.

The 2026 d-distance proof gives a new equality family for its own `d>=2` extension; it does not
supply the missing `d=1` integer-slack list.

## Support-core route and a stronger necessary restriction

TF14's support-core notation remains:

- H = support vertices, `h=|H|`;
- S = nonleaf non-support vertices, `s=|S|`;
- `delta=L-h`;
- `tau_H` = minimum number of vertices of S needed in addition to H to dominate T.

TF14 proved

`gamma=h+tau_H`

and, on the strict rounded branch,

`T is maximum iff tau_H=floor((s+2delta)/3)`.

TF15 found a useful independent sharpening from Abel Cabrera-Martínez,
“An improved upper bound on the domination number of a tree”,
*Discrete Applied Mathematics* 343 (2024), 44--48,
DOI `10.1016/j.dam.2023.10.013`.

Using that paper's notation, let `SL(T)` be the support-link vertices, `L_s(T)` the strong leaves,
and `S_s(T)` the strong supports. Its bound is

`3 gamma <= n+h-|SL|-|L_s|+|S_s|`.

For a tree of order at least three,

`|L_s|-|S_s| = L-h = delta`,

because each support contributes one “first” leaf and every additional leaf is counted in the
strong-leaf excess. Hence

`3 gamma <= n+h-|SL|-delta`.

For a strict-rounded residue-epsilon maximizer,

`3 gamma = n+L-epsilon = n+h+delta-epsilon`.

Comparison gives the exact necessary condition

`2 delta + |SL(T)| <= epsilon`.

Therefore:

- residue 1 forces `delta=0` and `|SL|<=1`;
- residue 2 forces either `delta=0` and `|SL|<=2`, or `delta=1` and `|SL|=0`.

This explains why extra leaves are exceptionally constrained in the final rounded cases and
connects the support-core and published domination-bound viewpoints.

It is **not** a complete iff replacement for the constructive defect theorem. Burned orders 1--14
already contain strict-rounded maximizers where the inequality is strict.

## Burned-order falsification only

The deterministic TF15 reproducer

`python -m experiments.tf15_segment_domination_rounded_defect`

uses only all 5,447 burned unlabeled trees through order 14.

It checks:

- the Cabrera-Martínez refined domination inequality on all 5,445 trees of order at least three;
- the identity `|L_s|-|S_s|=delta` on those same trees;
- the TF14 strict-rounded maximizer residue counts remain 49 / 119 / 49 for residues 0 / 1 / 2;
- every strict-rounded maximizer satisfies `2delta+|SL|<=epsilon`;
- the exact burned support profiles are:

| epsilon | delta | support links | burned maximizers |
|---:|---:|---:|---:|
| 0 | 0 | 0 | 49 |
| 1 | 0 | 0 | 50 |
| 1 | 0 | 1 | 69 |
| 2 | 0 | 0 | 33 |
| 2 | 0 | 1 | 3 |
| 2 | 0 | 2 | 5 |
| 2 | 1 | 0 | 8 |

The profile table is interpretation/falsification data only. It is not used to prove the infinite
defect theorem.

Two useful failures of over-strong support claims are preserved:

1. residue 1 does **not** force equality in `2delta+|SL|<=1`; the smallest burned profile with
   `(delta,|SL|)=(0,0)` occurs at order 10;
2. residue 2 does **not** force equality in `2delta+|SL|<=2`; the smallest burned profile with
   `(delta,|SL|)=(0,0)` already occurs at order 8.

Thus neither the 2024 equality family nor a rule such as “one support-link for residue 1” or
“one extra leaf/two support-links for residue 2” can classify all rounded maximizers.

No order-15 tree is generated or inspected.

## Complete fixed-segment maximum equality theorem

TF15 closes the final realization residue left by TF14.

For `q>=3`, take the numerical maximum `M=gamma_max(n,q)` and any optimizing leaf count

`max(ceil((q+3)/2),3M-n) <= L <= min(q,n-M)`.

Then every realization belongs to exactly one of the following complete branches:

1. `n-L <= floor((n+L)/3)`: it is maximum iff every nonleaf is a support.
   Status: **TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS**.
2. `floor((n+L)/3)<n-L` and `n+L == 0 (mod 3)`: it is maximum iff it is both a Favaron
   real-equality tree and a published `(gamma,i)`-tree.
   Status: **DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATIONS**.
3. `floor((n+L)/3)<n-L` and `n+L == 1 (mod 3)`: it is maximum iff it has the published
   P1-starting `(gamma,i)` construction whose defect walk ends at 1.
   Status: **TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS**.
4. `floor((n+L)/3)<n-L` and `n+L == 2 (mod 3)`: it is maximum iff it has the published
   P1-starting `(gamma,i)` construction whose defect walk ends at 2.
   Status: **TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS**.

Together with TF13's complete minimum equality theorem, this completes the fixed-(n,q)
domination extremal/equality programme at a recursive structural level.

## Theorem significance

The defect-1/2 result stays inside TreeForge.

Its content is useful because it converts the final integer saturation problem into an exact local
recurrence on a published complete construction. But the proof is short bookkeeping once the 2006
grammar is in hand, and the characterization is construction-recursive rather than a new canonical
geometric decomposition.

The support-link corollary is a useful structural sharpening but is only necessary, not sufficient.
No separate theorem repository is justified.

## Experiment and registry decision

New scientific experiment frozen: **no**.  
TF15-0001 created: **no**.  
Scientific experiment executed: **no**.  
TxGraffiti discovery run: **no**.  
New candidate allocated: **no**.  
Candidate registry changed: **no**.  
Experiment registry changed: **no**.  
Next permanent candidate: **TF-001158**.  
New default invariant added: **no**.  
TF4 MIS fan reopened: **no**.  
TF7--TF9 fixed-support thread reopened: **no**.  
Order 15 consumed: **no**.  
Orders at least 15 remain untouched: **yes**.

The TF15 defect counter, support-link count and strong-leaf bookkeeping are proof diagnostics only
and are not added to the invariant catalog.

The diagnosis JSON is generated by CI from the deterministic reproducer and uploaded as an Actions
artifact. TF15 does not imply that a committed diagnosis JSON exists.

## Fixed-segment thread decision

**CLOSE the fixed-segment thread.**

The numerical extrema, minimum equality classes, and maximum equality classes are now all resolved
to the standard justified in TreeForge: published classifications where available, plus explicitly
identified elementary structural reductions/bookkeeping where needed.

A TF16 continuation is not warranted merely to seek a prettier construction-independent description
of the same residue. TreeForge should return to a research-question pause. A future session should
begin from an independently motivated tree-theoretic question before any new experiment, candidate,
invariant, or fresh order is opened.
