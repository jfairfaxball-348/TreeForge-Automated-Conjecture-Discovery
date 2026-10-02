# TF4-0001 result

TF4-0001 is scientifically complete. Finite computation is evidence, not proof.

## Frozen change and provenance

Scientific source commit: `d8e0874a22dde7f226431fc4f15a36adb8254efa`  
Successful GitHub Actions run: `36983184665`

Exactly one material discovery axis changed from TF3: ratios-only generation became 21 fixed
pairwise `convex_hull` runs over the unchanged seven features, followed only by exact normalized
cross-run deduplication. The target, discovery orders, heuristics, post-processors, literal all-tree
hypothesis, and TxGraffiti pin remained frozen.

## Pairwise generation

- feature-pair runs: 21
- raw outputs: 259
- after Morgan: 259
- after Dalmatian: 214
- per-run post-duplicate total: 205
- cross-run exact unique statements: 146
- permanent IDs: `TF-001012` through `TF-001157`
- discovery-side reevaluation failures: 0
- exposed K1 failures: 47

All 146 cross-run unique statements received permanent IDs before the K1 consistency gate.

## Candidate-batch firewall

After discovery reevaluation and exposed K1 consistency, 99 candidates remained.
Candidate-batch SHA-256: `2bbb81b85eb6e40351f0913fafdc822c5417b2336e957e83fc08b505aedabf0f`.

The persisted freeze says `holdout_constructed: false`. Only after that file/hash existed did the
runner construct order 14.

## Fresh order-14 holdout

All 3159 unlabeled order-14 trees were tested.
SHA-256: `84978208ee2c65e3cda8327709e662cc71f9018ef2afc1ca03ff86a19a6197c3`.

- tested: 99
- falsified: 66
- survived: 33

## Frozen fresh hostile set

Exactly 19 pre-frozen hostile trees were constructed.
SHA-256: `caf97df7db6b739383e015f816e3d643352cf53f164363d171c0eb1751e955f3`.

Only the 33 order-14 survivors were tested; none failed this finite hostile gate.

## Mathematical interpretation

Post-gate interpretation used burned/exposed material freely and did not change the scientific run.

- `TF-001068` is falsified by an already-exposed order-11 tree.
- `TF-001015`, `TF-001021`, `TF-001027`, `TF-001032`, `TF-001078`, and
  `TF-001107` are elementary consequences and are `TRIVIAL`.
- `TF-001065`, `TF-001066`, `TF-001069`, and `TF-001070` are
  `ARTIFACT_OF_FEATURE_SET`: same-coefficient support/MIS facets are pointwise stronger because
  support_vertex_count <= leaf_count.
- `TF-001013` independently reached `MATHEMATICALLY_INTERESTING`, then a bounded audit found
  the exact Lemańska 2004 leaf bound; it is `KNOWN_RESULT`.
- `TF-001028` independently reached `MATHEMATICALLY_INTERESTING`; its bounded exact-form audit
  found related literature but no exact match. It remains `NOVELTY_AUDIT`; that negative search is
  explicitly not evidence of novelty.
- The remaining 20 finite survivors are all maximal-independent-set-count facets. They stay
  `ADVERSARIAL_PASSED` with interpretation notes only; no structural reason justified promotion.

Five of the 146 exact forms duplicate TF2 normalized relations:
`TF-001018, TF-001022, TF-001031, TF-001088, TF-001156`. All five were already falsified during TF4's computational gates.

Final interpreted lifecycle counts: {'ADVERSARIAL_PASSED': 20, 'ARTIFACT_OF_FEATURE_SET': 4, 'FALSIFIED': 114, 'KNOWN_RESULT': 1, 'NOVELTY_AUDIT': 1, 'TRIVIAL': 6}.

No candidate reaches `GRADUATION_CANDIDATE`; no theoremhood or novelty claim is made.

## Scientific conclusion

Pairwise hulls improved interpretability relative to TF2: every statement has at most two RHS
features, and the simple non-MIS survivors can be analyzed directly. They did not fully solve the
facet problem: maximal_independent_set_count still generated a large neighboring family of finite
survivors without a convincing structural mechanism.

TF5 should therefore not broaden the grammar immediately. It should first attack `TF-001028`
structurally (proof attempt, explicit family counterexample search, and focused prior-art completion).
Only if that resolves negatively should TreeForge freeze another discovery-axis change.
