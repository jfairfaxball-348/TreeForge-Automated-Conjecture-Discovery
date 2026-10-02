# TF5 structural analysis of TF-001028

TF5 resolves TF-001028 as a **KNOWN_RESULT consequence of stronger prior art**. No new
TreeForge theorem or novelty claim is made, and no new discovery experiment is frozen.

## Verified starting state

- starting main: 308104fee32f55dc12a110357c48f15249193be5
- successful post-TF4 main CI: 37016098699
- PR #10: merged
- TF2 authoritative source/run: d091d88889fa72322bfc49a5531bc30b1f31b049 / 36888114138
- corrected TF3 diagnostic run: 36907058956
- TF3 authoritative source/run: e23b44d24a7b87d6f67aa18749059540934b2767 / 36914647703
- TF4 diagnostic runs: 36972524602, 36973194898
- TF4 authoritative source/run: d8e0874a22dde7f226431fc4f15a36adb8254efa / 36983184665
- TF4 final main/CI checkpoint: 308104fee32f55dc12a110357c48f15249193be5 / 37016098699

TF4 reproducibility facts were rechecked from the committed manifest and registries: 21 pairwise
runs, 259 raw outputs, 214 after Dalmatian, 205 per-run post-duplicate outputs, 146 exact
cross-run forms, IDs TF-001012 through TF-001157, 47 K1 failures, 99-candidate batch hash
2bbb81b85eb6e40351f0913fafdc822c5417b2336e957e83fc08b505aedabf0f, order-14 hash
84978208ee2c65e3cda8327709e662cc71f9018ef2afc1ca03ff86a19a6197c3, 19-tree hostile hash
caf97df7db6b739383e015f816e3d643352cf53f164363d171c0eb1751e955f3, and exactly one
TF4-0001 experiment record. The next permanent ID remains TF-001158.

## Candidate dossier

Authoritative statement:

For every finite simple tree T,

gamma(T) <= (2 |V(T)| + 1 - diameter(T)) / 3.

Equivalent integer form:

3 gamma(T) + diameter(T) <= 2 |V(T)| + 1.

Source pair: (order, diameter). Discovery touch count: 7. The append-only lineage is
OBSERVED -> CONJECTURED -> HOLDOUT_PASSED -> ADVERSARIAL_PASSED ->
MATHEMATICALLY_INTERESTING -> NOVELTY_AUDIT, followed by the TF5 KNOWN_RESULT revision.
It survived literal-domain consistency, the complete order-14 holdout, and the frozen 19-tree TF4
hostile set. Those are finite historical facts, not proof.

## Structural resolution

Let n=|V(T)|, D=diameter(T), and gamma=gamma(T).

K1 has n=1, D=0, gamma=1, so equality holds.

For n>=2, split by diameter.

**Short-diameter regime.** Ore's theorem gives gamma <= floor(n/2) for every isolate-free graph.
If 2D <= n+2, then

3 gamma + D <= 3 floor(n/2) + D <= 2n+1.

**Long-diameter regime.** Gu, Meng, Zhang and Wan (2013), Lemma 2.3, determine the maximum
domination number among trees with fixed order n and diameter D when D >= n/2+1:

gamma <= n-D + ceil((2D-n-1)/3).

Put x=2D-n-1. Since 3 ceil(x/3) <= x+2 for every integer x,

3 gamma + D <= 3(n-D) + x + 2 + D = 2n+1.

For integer D, these regimes cover every nontrivial tree; for even n the boundary D=n/2+1
belongs to both. Hence TF-001028 follows directly from published stronger bounds.

Two explicit infinite equality mechanisms are useful checks:

- P_(3k+1) has gamma=k+1 and D=3k;
- the corona P_k o K1 for k>=2 has n=2k, gamma=k, and D=k+1.

No independent new proof claim is needed: the frozen statement is a corollary of prior art.

## Candidate-specific counterexample attack

All computation in this section is exposed interpretation work, not fresh validation. An independent
exact tree DP was used for domination number; a separate exact tree DP was used for maximal
independent-set count in the MIS diagnosis.

Exhaustive exposed orders 1 through 14 contain 5,447 unlabeled trees. There were zero failures of
the integer inequality. Equality counts by order 1 through 14 were:

1, 0, 0, 1, 0, 1, 1, 1, 1, 2, 2, 3, 3, 5.

At order 14, four equality trees have (D,gamma)=(11,6) and one has (8,7).

A further 24,048 parameter instances were checked across paths, stars, double stars, equal-arm and
arbitrary three-arm spiders, brooms, small exhaustive caterpillars, uniform caterpillars, combs, and
periodic branch gadgets. No counterexample occurred. This search did not cause the lifecycle
decision; the published implication did.

The deterministic analysis code and machine-readable results are in
experiments/tf5_analysis.py and experiments/TF5-TF001028/analysis_summary.json.

## Prior-art audit

The TF4 exact-form search found no exact statement and explicitly treated that only as negative
search evidence. TF5 broadened the same candidate-specific audit to fixed-order/fixed-diameter
extremal domination results.

1. O. Ore, Theory of Graphs, AMS Colloquium Publications 38 (1962): isolate-free graphs satisfy
   gamma(G) <= floor(n/2). This proves the short-diameter regime.
2. Z. Gu, J. Meng, Z. Zhang, J. E. Wan, "Some Upper Bounds Related with Domination Number,"
   Journal of the Operations Research Society of China 1 (2013), 217-225,
   DOI 10.1007/s40305-013-0012-0. Lemma 2.3 gives the exact maximum domination number for
   fixed (n,D) trees when D>=n/2+1; together with the ceiling estimate above it directly implies
   TF-001028 in the complementary regime.
3. A. Cabrera Martinez, "An improved upper bound on the domination number of a tree,"
   Discrete Applied Mathematics 343 (2024), 44-48, DOI 10.1016/j.dam.2023.10.013.
   This gives recent support-structure upper bounds; it is related but not needed for the implication.
4. J. Guo, J. Xue, R. Liu, "Laplacian eigenvalue distribution, diameter and domination number of
   trees," Linear and Multilinear Algebra 73 (2025), 763-775,
   DOI 10.1080/03081087.2024.2385991. This is recent diameter/domination work but does not
   supply the frozen upper bound.

The final classification is therefore KNOWN_RESULT by implication from stronger prior art, not an
exact rediscovery claim and not a novelty claim.

## Diagnosis of the 20 MIS-count survivors

The 20 unpromoted TF4 survivors are a facet fan, not 20 independent mechanisms. Their coordinate
supports split as:

- MIS only: 3
- support-vertex count + MIS: 6
- diameter + MIS: 9
- matching number + MIS: 2

Raw maximal_independent_set_count is strongly scale-dependent. Its exact range over exposed orders
10 through 14 is respectively [2,17], [2,32], [2,33], [2,64], [2,65]. However, this does
**not** produce the TF3-style coefficient drift: every one of the 20 frozen inequalities remains
valid and has equality examples separately at each exposed order 11, 12, 13, and 14. Thus none of
the 20 coefficient planes loses supporting status when those orders are included.

The fan also shares extremal geometry. The invariant vector

gamma=4, D=5, support=4, matching=4, MIS=8

makes 10 of the 20 candidates tight. Trees with that same vector occur 1, 2, 6, 10, 19, 28,
and 44 times at orders 8 through 14. On the entire exposed orders 1 through 14 corpus, only two
strict pointwise dominance relations occur among the 20: TF-001091 dominates TF-001034 and
TF-001095 dominates TF-001037. These are finite exposed-data dominance observations, not
universal theorem claims.

Diagnosis: the facet fan is genuine low-dimensional convex-hull geometry concentrated around
repeated invariant vectors. MIS count has awkward raw scale, but scale alone does not explain away
the coefficient stability. Therefore TF5 does **not** justify deleting MIS count, taking a logarithm,
or freezing another grammar change.

## Lifecycle and next step

TF-001028 moves append-only from revision 6 NOVELTY_AUDIT to revision 7 KNOWN_RESULT.
It does not reach GRADUATION_CANDIDATE. No new candidate ID is allocated; the next ID remains
TF-001158. No new scientific experiment registry record is created.

TF5 freezes no new experiment. The next session should remain diagnostic: determine whether there
is an independently mathematical reason to normalize, transform, or replace raw
maximal_independent_set_count, or whether the surviving fan should simply remain archived finite
geometry. Do not consume new fresh holdout data until a single-axis change is justified independently
of desired candidate yield.
