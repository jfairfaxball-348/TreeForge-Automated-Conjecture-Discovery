# Research protocol

## Corpora

Every experiment declares four logically distinct sources:

- **discovery corpus** — may be seen by the conjecturing engine;
- **holdout corpus** — frozen before generation and inaccessible to the engine;
- **targeted adversarial corpus** — hostile families selected after interpreting a candidate;
- **parametric families** — paths, stars, spiders, caterpillars, balanced trees, and other mathematically motivated constructions.

The initial implementation supports order-separated discovery and holdout corpora. TF1 must freeze exact order bounds only after timing the chosen invariant set. Conservative small bounds are preferred over an oversized census.

## Reproducibility record

Every generated dataset or experiment records the source commit, exact command, dependency versions, random seed if any, generation parameters, and SHA-256 of canonical serialised data. Large generated datasets should normally be regenerated from code rather than committed.

## Anti-numerology gates

Candidates are not promoted merely for fitting the discovery corpus. Required checks include holdout evaluation, deliberate smallest-counterexample search, structured hostile families, exact-vs-approximate tracking, duplicate/equivalent invariant detection where practical, definition/algebraic-consequence checks, and equality-case preservation.

Known tree identities are calibration targets only. A calibration rediscovery is labelled `KNOWN_RESULT` and `KNOWN/CALIBRATION`, not a research discovery.

## Discovery/proof firewall

Finite exhaustive certification is evidence about a finite range. It is not a proof of an infinite statement. Only a candidate that survives the research gates and passes mathematical interpretation plus a bounded prior-art audit may become `GRADUATION_CANDIDATE`. Graduation creates a separate repository.
