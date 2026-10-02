# TF9 — fixed-support MIS prior-art and theorem-significance audit

TF9 is a bounded bibliographic audit of the structural theorem proved in TF7 and sharpened in TF8.
It is not a new discovery experiment. No fresh tree order is consumed, no archived TF4 coefficient
fan is reopened, and a failed search is never treated as novelty evidence.

## Audited theorem

Write (m(T)) for the number of maximal independent sets of a finite tree (T),
(S(T)) for its support-vertex set, (s(T)=|S(T)|), (L(T)) for its leaves, and
(C(T)=V(T)\setminus(S(T)\cup L(T))). TF7/TF8 prove, for (s(T)\ge3),

[
m(T)\ge F_{s(T)+2},
]

with equality exactly for trees obtained from (P_s) by attaching at least one private leaf to every
path vertex and adding no other vertices. Equivalently the equality class is the arbitrary
duplicate-leaf closure of (P_s\circ K_1).

The proof package decomposes into:

1. (i(F)\ge F_{|V(F)|+2}) for forests, with equality only for a path;
2. (m(T)\ge i(T[S(T)])) for (T\ne P_2);
3. (m(T)=i(T[S(T)])) iff (T[C(T)]) is edgeless;
4. the fixed-support extremal value and complete equality class.

## Verified starting provenance

TF9 starts from merged TF8 main
`2dcf6df89648dab8b050b1ebf05f332dceb90c54`. PR #14 is merged; its exact head is
`395ae9befe2e858a47fc73d2d00e30ad53e6427f`, exact PR-head CI `37059137030` passed,
and post-merge CI `37059395616` passed.

The committed TF8 reproducer verifies the current registry boundary: TF-001028 is
`KNOWN_RESULT` revision 7; TF-001034 and TF-001037 are `ARTIFACT_OF_FEATURE_SET`
revision 6; TF-001091 and TF-001095 are revision-5 `ADVERSARIAL_PASSED`; the remaining
sixteen active TF4 MIS facets are also revision-5 `ADVERSARIAL_PASSED`. TF-001157 is the
highest allocated candidate and TF-001158 remains next. There is exactly one TF4-0001 experiment
registry row and no TF5--TF8 scientific experiment row.

Orders 1--14 are burned. Orders at least 15 remain untouched throughout TF9.

## Search scope

The bounded search used combinations and terminology variants around:

- maximal independent sets / number of maximal independent sets;
- independent dominating sets / independent domination polynomial;
- Merrifield--Simmons index / Fibonacci index / independent sets in trees;
- support vertices / preleaves / stems / pendant vertices;
- fixed support, fixed number of supports, fixed leaves, fixed matching number, fixed independence
  number, twin-free trees, coronas, and extensions.

Sources inspected included original or publisher pages/full texts where accessible: SIAM, Elsevier
ScienceDirect, the HSE open manuscript of Taletskii--Malyshev (2022), the arXiv manuscript and final
journal metadata for Tian--Tu (2025), Electronic Journal of Combinatorics, The Fibonacci Quarterly
catalog/Taylor & Francis metadata, De Gruyter metadata, DBLP, and author/institution publication
metadata. Exact-phrase failure was not used as a novelty criterion.

A terminology warning matters: Taletskii--Malyshev use *preleaf* in their twin-leaf work for the
support-vertex notion, while *stem* is not uniform across the literature.

## Component A — all independent sets of a forest

**Status: DIRECT_COROLLARY of classical prior art.**

H. Prodinger and R. F. Tichy, *Fibonacci Numbers of Graphs*, The Fibonacci Quarterly 20(1)
(1982), 16--21, DOI 10.1080/00150517.1982.12430021, prove for every (n)-vertex tree (T)

[
F_{n+2}\le i(T)\le 2^{n-1}+1,
]

with equality in the lower bound iff (T=P_n), and equality in the upper bound iff (T=K_{1,n-1}).
Thus the tree case, including path uniqueness, is classical.

The forest formulation used by TreeForge is an elementary direct corollary. If a forest (F) is
disconnected, adding bridges between components produces a tree on the same vertex set and strictly
removes independent sets, so equality with the tree lower envelope cannot occur. Hence
(i(F)\ge F_{|V(F)|+2}), with equality iff (F=P_{|V(F)|}).

The TF8 forest-equality lemma therefore should not be presented as independent new mathematics.

## Component B — support-induced injection

**Status: no exact statement located in this bounded audit; related recurrences and special cases are
published. Negative search is not novelty evidence.**

For (T\ne P_2), TF7 injects independent subsets of (S(T)) into disjoint nonempty classes of
maximal independent sets and obtains

[
m(T)\ge i(T[S(T)]).
]

The closest primary-source mechanisms located are:

- Y. Tian and J. Tu, *The minimum number of maximal independent sets in graphs with given order and
  independence number*, Discrete Applied Mathematics 368 (2025), 52--65,
  DOI 10.1016/j.dam.2025.02.027. Their Lemma 3 gives the support-vertex recurrence
  (mis(G)=mis(G-Q-y)+mis(G-N[y])), where (Q) is the leaf set adjacent to a support (y).
  Relationship: **RELATED_ONLY** to the injection itself.
- D. S. Taletskii and D. S. Malyshev, *The number of maximal independent sets in trees with a given
  number of leaves*, Discrete Applied Mathematics 314 (2022), 321--330,
  DOI 10.1016/j.dam.2022.03.012. Their Lemma 4 proves
  (i(H)=mi(ext(H))), where (ext(H)=H\circ K_1).
  Relationship: **SAME_INGREDIENT_DIFFERENT_PARAMETER**; it is the corona equality special case,
  not the general support-induced injection.

Wilf's tree DP and Ortiz--Villanueva's caterpillar enumeration supply broader enumeration
recurrences, but no exact support-set injection was located.

## Component C — equality in the support injection

**Status: no exact published match located; apparently elementary/unisolated under this bounded
audit.**

TF8 proves

[
m(T)=i(T[S(T)]) \quad\Longleftrightarrow\quad T[C(T)]\text{ is edgeless}
]

for every finite tree (T\ne P_2). Tian--Tu's support recurrence makes support decomposition
natural, but their theorem does not state this criterion. Taletskii--Malyshev's extension lemma gives
the special case with empty core. Searches under support/preleaf, independent domination, maximal
independent set enumeration, and support-induced terminology did not locate the iff statement.

This is the part of the TF7/TF8 proof package least clearly represented in the located literature.
That is only a bounded-search status, not a novelty claim.

## Component D — fixed-support extremal value

**Status: DIRECT_COROLLARY of a STRICTLY_STRONGER_RESULT.**

Tian--Tu (2025), Theorem 1, prove for every tree (T) of order (n) and independence number
(alpha)

[
m(T)\ge F_{n-\alpha+2},
]

and show the bound is sharp. Their published journal statement has the (+2); the older arXiv-v1
abstract displays a stale (F_{n-\alpha}), while Theorem 1 inside that same manuscript and the
final journal abstract use (F_{n-\alpha+2}).

For a tree, bipartiteness plus König/Gallai gives (n-\alpha(T)=\nu(T)), the maximum matching
number. For (T\ne P_2), choose one private leaf adjacent to each support vertex. Those
support--leaf edges are pairwise disjoint, so

[
s(T)\le\nu(T).
]

Therefore

[
m(T)\ge F_{\nu(T)+2}\ge F_{s(T)+2}.
]

For every (s\ge3), Tian--Tu's sharp construction at (n=2s,alpha=s) is
(P_s\circ K_1), so the fixed-support lower bound is attained. Consequently the TF7 exact
fixed-support **value** theorem for (s\ge3) is a direct corollary of published stronger prior art
plus the elementary matching observation.

The exceptional (P_2) is exactly where the simple support-to-private-leaf matching argument fails,
because its vertices are simultaneously leaves and supports.

## Equality family versus stronger prior art

Tian--Tu prove sharpness by exhibiting an extremal family, but the inspected theorem/manuscript does
not characterize every tree attaining equality; no "if and only if" or equality classification for
their tree bound was located. At (n=2s,alpha=s) their construction gives (P_s\circ K_1), but
this alone does not imply TF8's complete fixed-support minimizer class.

Taletskii--Malyshev (2022) supply two more already-known ingredients:

- (i(H)=mi(H\circ K_1));
- adding a leaf twin to an existing leaf does not change (mi).

Thus the **if** direction for arbitrary duplicate-leaf blowups of (P_s\circ K_1) is assembled from
published ingredients plus the classical path independent-set count. The TF8 **only-if** statement,
and especially the core-edgeless injection-equality lemma that drives it, were not found as exact
published statements in this bounded audit.

Accordingly the complete equality classification is **not shown here to be a direct corollary** of
the sources located, but neither is it claimed novel.

## Fixed-leaf and other MIS literature

- H. S. Wilf, *The Number of Maximal Independent Sets in a Tree*, SIAM Journal on Algebraic and
  Discrete Methods 7(1) (1986), 125--130, DOI 10.1137/0607015: fixes order and maximizes MIS count;
  also gives a linear-time tree recurrence. **RELATED_ONLY**.
- B. E. Sagan, *A Note on Independent Sets in Trees*, SIAM Journal on Discrete Mathematics 1(1)
  (1988), 105--108, DOI 10.1137/0401012: simplified proof and characterization of Wilf's
  order-wise maximum. **RELATED_ONLY**.
- C. Ortiz and M. Villanueva, *Maximal independent sets in caterpillar graphs*, Discrete Applied
  Mathematics 160(3) (2012), 259--266, DOI 10.1016/j.dam.2011.10.024: enumerates MIS in
  caterpillars; no fixed-support extremal theorem. **RELATED_ONLY**.
- D. S. Taletskii and D. S. Malyshev (2022), DOI 10.1016/j.dam.2022.03.012: fixes both order and
  number of leaves and describes maximum/minimum trees. Their minimum tree is a path
  (P_{n-l+2}) with the extra (l-2) leaves attached at penultimate path vertices. This is a
  genuinely different conditioning problem and does not imply the fixed-support classification.
  **SAME_INGREDIENT_DIFFERENT_PARAMETER**.
- D. S. Taletskii and D. S. Malyshev, *Trees without twin-leaves with smallest number of maximal
  independent sets*, Discrete Mathematics and Applications 30(1) (2020), 53--67,
  DOI 10.1515/dma-2020-0006: fixes order under a twin-leaf prohibition and characterizes minimum
  trees. **SAME_INGREDIENT_DIFFERENT_PARAMETER**.
- S. Cambie and S. Wagner, *The Minimum Number of Maximal Independent Sets in Twin-Free Graphs*,
  Electronic Journal of Combinatorics 31(4) (2024), P4.71, DOI 10.37236/12789: gives a shorter
  treatment of the twin-free minimum problem, again order-conditioned. **SAME_INGREDIENT_DIFFERENT_PARAMETER**.

The fixed-leaf theorem does not secretly settle fixed support: its parameter pair is ((n,l)), and
its minimum family generally has a small support set concentrated near the path ends. Conversely
fixed support allows arbitrarily many duplicate leaves without changing (m) or (s).

## Theorem-significance assessment

Support count is a standard local tree parameter and the TF8 core criterion is a clean structural
lemma. Nevertheless, the principal extremal value is already subsumed by Tian--Tu's stronger
(n-\alpha=\nu) lower bound, the path independent-set ingredient is classical, and the corona plus
twin-leaf invariances are explicitly present in Taletskii--Malyshev.

What remains potentially independent is therefore an equality-only sharpening: the exact
support-induced equality criterion and the proof that no other fixed-support minimizers exist. The
proof is short and elementary, and the bounded audit does not reveal a separate research program
that depends on it. Citation scarcity alone is not enough to manufacture such a program.

**Decision: keep the result internal to TreeForge; do not create a separate theorem-focused
repository in TF9.** A later expert or exhaustive bibliographic review could revisit the equality-only
status, but the present evidence does not justify theorem packaging, Lean/Palomar work, or a paper
project.

## TreeForge consequences

- Candidate lifecycle event: **none**.
- TF4 MIS fan reopened: **no**; the 18 revision-5 finite survivors stay archived.
- Raw `maximal_independent_set_count`: **retain unchanged**.
- New coordinate or grammar change: **none**.
- Scientific experiment frozen: **none**.
- Candidate ID allocated: **none**; TF-001158 remains next.
- Candidate registry changed: **no**.
- Experiment registry changed: **no**.
- Fresh exhaustive data consumed: **no**; orders at least 15 remain untouched.
- Separate theorem repository: **not justified**.

## Bounded-audit limitation and stopping rule

This record establishes only what was found and how the located results imply TreeForge's theorem.
It does **not** establish novelty of the equality-only statements. In particular, no conclusion is
drawn from an exact-string search failure, and an equivalent result under different terminology may
still exist.

The defensible next TreeForge session is therefore not another MIS-fan session. Keep orders at least
15 untouched until a separately motivated discovery question identifies a controlled axis. Revisit
the equality-only theorem outside TreeForge only if later expert bibliographic review provides an
independent reason to do so.
