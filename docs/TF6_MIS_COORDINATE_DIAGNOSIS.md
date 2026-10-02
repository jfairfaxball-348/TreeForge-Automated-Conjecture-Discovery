# TF6 maximal-independent-set-count coordinate diagnosis

TF6 is an exposed-data diagnosis, not a new scientific experiment. It starts from verified
post-TF5 `main` commit
`1a0bd2363908659a76ebba8a9d0cc1662f4b4980`, whose post-merge CI run
`37032824545` succeeded. PR #11 is merged. No order above 14 is inspected here, no new
holdout is allocated, and the TF5 family instances remain burned interpretation data.

## Provenance recheck

The authoritative earlier scientific records remain unchanged:

- TF2: source `d091d88889fa72322bfc49a5531bc30b1f31b049`, run `36888114138`.
- TF3: corrected diagnostic run `36907058956`; source
  `e23b44d24a7b87d6f67aa18749059540934b2767`, run `36914647703`.
- TF4: diagnostic runs `36972524602`, `36973194898`; source
  `d8e0874a22dde7f226431fc4f15a36adb8254efa`, run `36983184665`.
- TF5: PR #11; final main `1a0bd2363908659a76ebba8a9d0cc1662f4b4980`; final
  post-merge CI `37032824545`.

The experiment registry still contains exactly one `TF4-0001` record and no TF5 scientific
experiment record. TF-001028 has revisions 1 through 7 in order and ends at revision 7 in
`KNOWN_RESULT`; it never reached `GRADUATION_CANDIDATE`. The highest allocated permanent
candidate is TF-001157, so TF-001158 remains next.

## The exact 20-candidate fan

Write (gamma) for domination number, (m) for
`maximal_independent_set_count`, (s) for support-vertex count, (D) for diameter, and
(
u) for matching number. All 20 rows below remain finite `ADVERSARIAL_PASSED`
survivors. Each passed the frozen order-14 holdout and TF4 hostile set. The last four columns
are equality counts on the already exposed orders 11, 12, 13, and 14.

| ID | frozen relation | discovery touches | eq11 | eq12 | eq13 | eq14 |
|---|---|---:|---:|---:|---:|---:|
| TF-001033 | (gammale m/2+1/2) | 38 | 16 | 21 | 25 | 31 |
| TF-001034 | (gammale m/3+4/3) | 31 | 22 | 35 | 48 | 69 |
| TF-001037 | (gammale m/5+12/5) | 10 | 13 | 28 | 47 | 82 |
| TF-001090 | (gammale -s+1+m) | 39 | 16 | 21 | 25 | 31 |
| TF-001091 | (gammale 2s/5+4/5+m/5) | 37 | 25 | 38 | 52 | 73 |
| TF-001093 | (gammale 3s/7+8/7+m/7) | 19 | 19 | 32 | 47 | 69 |
| TF-001095 | (gammale 3s/8+3/2+m/8) | 14 | 19 | 38 | 62 | 103 |
| TF-001098 | (gammage 9s/4-3-m/4) | 11 | 13 | 28 | 47 | 82 |
| TF-001099 | (gammale 5s/9+10/9+m/9) | 11 | 10 | 15 | 21 | 28 |
| TF-001134 | (gammale -D+2+m) | 85 | 41 | 53 | 66 | 81 |
| TF-001135 | (gammale -D/2+5/2+m/2) | 60 | 46 | 69 | 99 | 137 |
| TF-001137 | (gammale D/4+3/4+m/4) | 38 | 29 | 46 | 64 | 92 |
| TF-001139 | (gammale D/6+11/6+m/6) | 18 | 24 | 50 | 87 | 151 |
| TF-001140 | (gammage 3D/2-3-m/2) | 15 | 7 | 9 | 10 | 12 |
| TF-001141 | (gammale -D/4+13/4+m/4) | 13 | 19 | 38 | 66 | 110 |
| TF-001142 | (gammale 3D/8+11/8+m/8) | 9 | 13 | 26 | 47 | 81 |
| TF-001144 | (gammale -5D/4+29/4+m/2) | 9 | 9 | 15 | 20 | 28 |
| TF-001145 | (gammale -3D+15+m) | 7 | 5 | 7 | 8 | 10 |
| TF-001154 | (gammage 2
u+1-m) | 34 | 8 | 10 | 10 | 12 |
| TF-001155 | (gammage 5
u/2-3-m/2) | 20 | 15 | 23 | 31 | 42 |

The source-coordinate distribution is exactly 3 MIS-only, 6 support/MIS, 9 diameter/MIS, and
2 matching/MIS. There are 16 upper bounds and 4 lower bounds. The machine-readable dossier
also preserves every exact normalized statement, constant and coefficient, source pair, discovery
equality example, holdout/hostile status, lifecycle state, and cumulative exposed support count.

## Coefficient stability and facet geometry

Recomputation uses only the 5,447 already exposed unlabeled trees of orders 1--14. On the
discovery corpus (orders 2--10) and after cumulative extension through each of orders 11, 12,
13, and 14, every one of the 20 frozen inequalities has zero failures and at least one equality.
Thus every frozen plane remains a supporting hyperplane of its exposed sample at every extension.
This is materially different from TF3's visibly drifting ratio coefficients.

No two candidates have exactly the same equality-tree set through order 14, and no two have
exactly the same equality-invariant-vector set. They are therefore not merely duplicate statements
under a different coefficient spelling.

The strongest shared discrete support is nevertheless substantial. The vector

[
(gamma,D,s,
u,m)=(4,5,4,4,8)
]

makes ten candidates tight:
TF-001034, TF-001037, TF-001091, TF-001093, TF-001095, TF-001098, TF-001135,
TF-001137, TF-001139, and TF-001141. It occurs on 110 exposed trees in total, with counts
1, 2, 6, 10, 19, 28, and 44 at orders 8 through 14. Other repeated vectors similarly support
smaller groups. The fan is therefore genuine low-dimensional discrete convex geometry concentrated
around recurrent invariant vectors, not a collection of exact duplicates.

The TF5 dominance result also reproduces exactly. The only strict pointwise dominance relations on
the entire exposed corpus are:

- TF-001091 over TF-001034;
- TF-001095 over TF-001037.

Algebraically, the first would be universal exactly if
(mge 3s-4), and the second exactly if (mge 5s-12). TF6 verifies those conditions only on the
exposed corpus; it does **not** promote them to tree theorems. Elementary facts such as
(sle
u) and the matching available on a longest path do not by themselves imply either
MIS/support inequality.

Two MIS-only facets can therefore be viewed as exposed projections that are improved by adding
support count, but TF-001033 is not pointwise dominated by another member of this 20-facet set.

## Exact structural recurrence for MIS count

A maximal independent set is exactly an independent dominating set. This gives
`maximal_independent_set_count` a direct domination-theoretic meaning independent of any TF4
coefficient.

Root a tree and let a subtree state be:

- (A): the root is selected;
- (B): the root is not selected but is dominated by a selected child;
- (C): the root is not selected and must be dominated by its parent.

For children (u),

[
 A_v=prod_u(B_u+C_u),qquad
 C_v=prod_u B_u,qquad
 B_v=prod_u(A_u+B_u)-prod_u B_u,
]

and the unrooted count is (m(T)=A_r+B_r). TF6 installs this exact three-state DP as the core
implementation and checks it independently against brute-force enumeration through order 8. This
is an implementation improvement only: the mathematical invariant and all historical corpus values
are unchanged.

The recurrence makes several local mechanisms explicit.

A leaf child has state ((1,0,1)). Adding a first leaf to a parent whose current local state is
((A,B,C)) sends it to ((A,B+C,0)). Adding further twin leaves at that same support vertex then
does nothing to the state. Thus duplicating a leaf at an existing support vertex leaves the
whole-tree MIS count unchanged. Stars illustrate the extreme case: every nontrivial star has
exactly two maximal independent sets regardless of order.

More generally, attach a rooted branch with state ((a,b,c)). The parent's local state transforms
as

[
(A,B,C)mapsto((b+c)A,,(a+b)B+aC,,bC).
]

With (q) identical branch children at a root, the total count is

[
(b+c)^q+(a+b)^q-b^q.
]

The raw exponential behavior is therefore a direct product phenomenon in the recurrence.

Path extension gives another regime. Exact DP yields

[
m(P_n)=m(P_{n-2})+m(P_{n-3})quad(nge4),
]

starting (1,2,2); path counts hence have Padovan-type exponential growth. For the corona
(extension) (Hcirc K_1), every maximal independent set chooses exactly one of each base
vertex/private-leaf pair, so maximal independent sets of the corona are in bijection with **all**
independent sets of (H). In particular, path coronas have Fibonacci-scale counts. Periodic
caterpillars and repeated spider arms compose the same finite state messages and consequently admit
transfer recurrences as well.

These examples show why “MIS grows exponentially” is too crude. The same invariant can be
constant under twin-leaf duplication, Padovan-like along path subdivision, Fibonacci-like on path
coronas, or multiplicative under repeated branches.

## Bounded structural literature check

TF6 searched only questions needed to understand this coordinate.

Wilf (1986) determined the largest possible number of maximal independent sets in an (n)-vertex
tree. Sagan (1988) gave a short graph-theoretic proof and characterization. The exact envelope is

[
m_{max}(2k)=2^{k-1}+1,qquad m_{max}(2k+1)=2^k.
]

So the exponential raw scale is extremally sharp, not a plotting artifact.

Taletskii and Malyshev (2022) determine maximum and minimum MIS counts for trees with fixed order
and leaf count. Their extension construction also records the identity
(mi(operatorname{ext}(T))=i(T)), the corona bijection used above. A 2012 paper devoted to
maximal independent sets in caterpillar graphs further confirms that recurrence/structure, rather
than one universal scalar rescaling, is natural for this enumerative parameter.

Sources:

- H. S. Wilf, *The Number of Maximal Independent Sets in a Tree*, SIAM J. Algebraic Discrete
  Methods 7 (1986), 125--130, DOI 10.1137/0607015.
- B. E. Sagan, *A Note on Independent Sets in Trees*, SIAM J. Discrete Math. 1 (1988),
  105--108, DOI 10.1137/0401012.
- D. S. Taletskii and D. S. Malyshev, *The number of maximal independent sets in trees with a
  given number of leaves*, Discrete Appl. Math. 314 (2022), 321--330,
  DOI 10.1016/j.dam.2022.03.012.
- *Maximal independent sets in caterpillar graphs*, Discrete Appl. Math. 160 (2012), 259--266,
  DOI 10.1016/j.dam.2011.10.024.

This is structural background, not a novelty audit of any TF4 survivor.

## Transformation audit

**Raw (m): retain for now.** It is exact, root-independent, combinatorial, recurrence-natural, and
the current fan does not exhibit exposed coefficient drift. Its scale is awkward for linear
conjecturing, but awkward scale is not an independent removal criterion.

**(log m): reject for now.** Logarithms have a clear enumerative meaning, but the tree recurrence
contains sums and differences as well as products. A logarithm therefore does not linearize general
tree composition, and it replaces exact rational convex-hull arithmetic with non-exact real
coordinates without a structural reason for (gamma) to depend linearly on (log m).

**((log m)/n) or (m^{1/n}): reject for now.** These are meaningful asymptotic growth-rate
diagnostics, but they couple the feature to order and throw away absolute count scale. No
candidate-independent theorem or recurrence makes domination linear in either quantity.

**(m/m_{max}(n)): reject for now.** This is an exact, independently meaningful normalization by
the Wilf/Sagan envelope. It is the strongest normalization considered in TF6, but it explicitly
mixes order into the coordinate and measures relative extremality rather than MIS multiplicity.
Nothing in the exposed fan or recurrence says (gamma) should be linear in that fraction.

**A recurrence-state coordinate: reject as a single replacement for now.** The triple ((A,B,C))
is structurally excellent for composition, but it depends on a chosen root. Turning it into one
root-invariant number requires a further aggregation choice; choosing that aggregation to improve
TF4 output would be bespoke fitting.

The sign pattern in the current fan is also diagnostic: all upper facets have positive MIS
coefficient and all lower facets have negative MIS coefficient. On families where (m) is
exponential while (gamma,s,D,
u) are at most linear in order, such inequalities can become
asymptotically loose rather than false. That is a real limitation of interpretability, but it does
not erase their sharp low-(m) regimes and is not enough to justify a coordinate change.

## TF6 decision

**Raw `maximal_independent_set_count`: retain unchanged for discovery purposes for now.**

**New controlled experiment frozen: no.**

**Fresh data allocated or consumed: no.**

**Candidate IDs allocated: none. TF-001158 remains next.**

The negative result is deliberate. TF6 found a mathematical explanation for the coordinate's
scale but no independently canonical removal or transformation. Freezing “remove MIS”, “log MIS”,
or “normalize MIS” now would choose an axis because it changes output volume/geometry, not because
tree mathematics selects it.

A following session should keep all orders at least 15 untouched. If the MIS question is continued,
the cleanest structural targets are the two exposed support/MIS dominance conditions
(mge3s-4) and (mge5s-12), or a root-invariant transfer statistic defined independently of
candidate yield. Otherwise the 20-facet fan should remain archived finite geometry while TreeForge
chooses a separately motivated scientific question. Neither route requires broadening the
TxGraffiti grammar.
