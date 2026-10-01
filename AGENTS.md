# TreeForge agent rules

1. Treat this repository as discovery/falsification/provenance infrastructure, not as a proof repository.
2. Never state or imply that finite testing proves an all-tree theorem.
3. Never infer novelty from a negative search. Record search scope and uncertainty.
4. Never formalise speculative candidates in Lean or package them for Palomar here.
5. Never create paper/arXiv packaging for candidates that have not graduated.
6. Do not use holdout objects for conjecture generation. If a holdout object leaks into discovery, invalidate the experiment and record the failure.
7. Candidate IDs are permanent. Append revisions and lifecycle events; never rewrite a failed conjecture out of history.
8. Counterexamples, duplicate detections, feature artifacts, and failed approaches are research outputs. Preserve them.
9. Invariants require definitions, provenance, tests, and exact/approximate classification before use.
10. Prefer exact integer/rational arithmetic. Approximation must be explicit in names, metadata, and documentation.
11. TxGraffiti is accessed only through `treeforge.conjecturing.txgraffiti_adapter`.
12. A candidate may graduate only after holdout/adversarial survival, mathematical interpretation, and a bounded prior-art audit.
