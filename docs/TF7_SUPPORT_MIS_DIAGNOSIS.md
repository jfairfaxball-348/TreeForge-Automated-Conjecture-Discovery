# TF7 support/MIS structural diagnosis

TF7 resolves the two support/MIS dominance conditions exposed by TF6. This is structural
mathematics and exposed-data diagnosis, not a new controlled discovery experiment. No exhaustive
tree of order at least 15 is inspected.

## Verified starting state

TF7 starts from the merged TF6 `main` commit
`3d4b3035301e681a7a5eed0facb2f5068051c746`. PR #12 is merged and the post-merge
Actions run `37047300108` is successful. The authoritative TF2, TF3, and TF4 scientific
runs remain unchanged, TF-001028 remains `KNOWN_RESULT` revision 7, TF-001157 remains the
highest allocated candidate, and TF-001158 remains next.

The experiment registry still contains exactly one `TF4-0001` row and no TF5, TF6, or TF7
scientific experiment row.

Write

- (m(T)) for `maximal_independent_set_count`;
- (S(T)) for the support-vertex set;
- (s(T)=|S(T)|); and
- (i(F)) for the number of all independent sets of a forest (F).

The TF6 dominance conditions were

[
m(T)ge 3s(T)-4
]

and

[
m(T)ge 5s(T)-12.
]

TF6 had verified them only on exposed data. TF7 proves both for every finite tree.

## Support-induced-forest mechanism

The key statement is stronger than either linear inequality.

**Proposition.** If (T
eq P_2), then

[
m(T)ge i(T[S(T)]).
]

For (K_1) the statement is immediate. Now let (T) have order at least three. Leaves and
support vertices are then disjoint. For every independent set (I) of the induced forest
(T[S(T)]), begin an independent set in (T) by taking

1. every support vertex in (I); and
2. every leaf whose support neighbor is not in (I).

The resulting set is independent. Extend it to any maximal independent set of (T). Every support
outside (I) already has one of its leaf neighbors selected, so no such support can enter the
extension; every support in (I) was selected initially. Thus every extension has support
intersection exactly (I).

Consequently distinct independent sets (Isubseteq S(T)) seed disjoint nonempty classes of
maximal independent sets of (T). Hence (m(T)ge i(T[S(T)])).

The tree (P_2) is the sole structural exception because both of its vertices are simultaneously
leaves and support vertices: (s(P_2)=2) and (m(P_2)=2), while its support-induced edge has
three independent sets.

This mechanism also handles adjacent support vertices automatically: their adjacency is simply an
edge of the forest (T[S(T)]). No separate exceptional recurrence is required.

## Fibonacci lower bound for the support forest

Let (F_0=0,F_1=1). Every forest (F) on (s) vertices satisfies

[
i(F)ge F_{s+2}.
]

The proof is an elementary induction on (s). For (s=0,1) the values are (1) and (2).
If (F) has an isolated vertex (v), then
(i(F)=2i(F-v)ge2F_{s+1}ge F_{s+2}).
Otherwise choose a leaf (v) with neighbor (u). Partition independent sets according to
whether they contain (v):

[
i(F)=i(F-v)+i(F-{u,v})
    ge F_{s+1}+F_s
    =F_{s+2}.
]

Combining this with the support-induced-forest proposition gives

[
oxed{m(T)ge F_{s(T)+2}}
]

for every finite tree other than (P_2).

This is a structural proof, not a finite-data extrapolation.

## Exact fixed-support minimum

The fixed-support extremal problem therefore has the exact value

[
min{m(T):s(T)=s}=
egin{cases}
1,&s=0,\
2,&s=1,\
2,&s=2,\
F_{s+2},&sge3.
end{cases}
]

The exceptional (s=2) minimum is (P_2). If one restricts to trees of order at least three,
the (s=2) minimum is (3).

For every (sge3), equality is attained by the corona (P_scirc K_1). Each base-path vertex
is a support vertex, and maximal independent sets of the corona are in bijection with all
independent sets of (P_s); hence
(m(P_scirc K_1)=i(P_s)=F_{s+2}).

TF6 already proved another useful reduction: once a support vertex has one leaf neighbor,
duplicating that leaf does not change (m(T)). Deleting duplicate leaves while retaining one
therefore preserves both (m(T)) and (s(T)). Thus fixed-support extremal analysis may reduce to
one leaf per support without changing the objective.

TF7 does not claim here to characterize every equality tree. The exact minimum and an infinite
attaining family are sufficient for the two dominance questions.

## The two TF6 inequalities

The Fibonacci theorem immediately proves both target inequalities.

For (m(T)ge3s(T)-4), the cases (sle2) are direct. For (sge3),
(F_{s+2}ge3s-4): equality begins at (s=3), and each subsequent Fibonacci increment
(F_{s+1}) is at least (3).

For (m(T)ge5s(T)-12), the cases (sle3) are direct. At (s=4),
(F_6=8=5s-12), and each subsequent Fibonacci increment (F_{s+1}) is at least (5).

Therefore both TF6 dominance conditions are universal tree inequalities.

## Candidate consequences

This result changes the interpretation of exactly two TF4 survivors.

For TF-001091 versus TF-001034, the two upper-bound right-hand sides are

[
R_{91}=rac{m+2s+4}{5},
qquad
R_{34}=rac{m+4}{3}.
]

Algebraically (R_{91}le R_{34}) exactly when (mge3s-4). Since TF7 proves that condition
for every finite tree, TF-001091 universally pointwise dominates TF-001034. TF-001034 therefore
receives an append-only revision from `ADVERSARIAL_PASSED` to
`ARTIFACT_OF_FEATURE_SET`.

Likewise

[
R_{95}=rac{m+3s+12}{8},
qquad
R_{37}=rac{m+12}{5},
]

and (R_{95}le R_{37}) exactly when (mge5s-12). TF-001095 therefore universally
pointwise dominates TF-001037, which receives the same append-only
`ARTIFACT_OF_FEATURE_SET` classification.

These transitions do **not** prove TF-001091 or TF-001095 as domination-number theorems. Both
stronger siblings remain revision-5 `ADVERSARIAL_PASSED` finite survivors. The TF7 result proves
only their universal pointwise superiority over the two MIS-only projections.

No historical TF4 record is deleted or rewritten.

## Exposed computational check

The deterministic reproducer recomputes only the already burned exhaustive orders 1--14:
5,447 unlabeled trees. It verifies, as interpretation data rather than proof, that

- the support-induced-forest lower bound has no failure except the explicitly isolated (P_2)
  mechanism;
- the Fibonacci bound has no failure except (P_2);
- both linear inequalities have zero failures;
- the exposed fixed-support minima are
  (1,2,2,5,8,13,21,34) for (s=0,ldots,7); and
- the path coronas for (s=3,ldots,7), all within order 14, attain the Fibonacci values.

No order 15 tree or other fresh exhaustive corpus is generated or inspected.

## Coordinate and experiment decision

Raw `maximal_independent_set_count` remains retained unchanged.

TF7 gives the coordinate more structural content, not less: fixed support count forces a sharp
Fibonacci lower envelope. That explains the two exposed dominance relations and shows that two
MIS-only TF4 facets are projection artifacts. It does not independently select a logarithm,
growth-rate normalization, removal of MIS, a rooted-state replacement, a new invariant, a wider
grammar, or any other single discovery-axis change.

The residual 18 MIS facets therefore remain archived finite geometry. None is promoted merely
because two neighboring projections became redundant.

New scientific experiment frozen: **no**.

Fresh exhaustive order consumed: **no**.

New candidate ID allocated: **no**.

Experiment registry updated: **no**.

The next permanent candidate ID remains `TF-001158`, and orders at least 15 remain untouched.

The deterministic machine record is
`experiments/TF7-DIAG-0001/diagnosis.json`, reproduced by
`python -m experiments.tf7_support_mis_diagnosis`.

## Next session

Keep orders at least 15 untouched until an independently motivated controlled axis exists. The
fixed-support Fibonacci theorem and its equality mechanisms are legitimate structural mathematics,
but they do not force a new TreeForge discovery experiment. A later session may study equality
classification for the fixed-support theorem or choose a separately motivated scientific question;
the remaining TF4 MIS fan should stay archived unless such mathematics supplies a new reason to
revisit it.
