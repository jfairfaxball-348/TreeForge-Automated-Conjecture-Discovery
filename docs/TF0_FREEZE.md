# TF0 infrastructure freeze

Date: 2026-10-01

## Read-only source lineage pins

- TreeStack `main`: `e1e437b8d02552b7c7ee0c4c74041b6ac956f063`
- ProbStack `main`: `ced67339f9289364a8c131bf2036af0502e2c08c`
- Greedy Uniformity `main`: `2fb997397daa8c16b80dd1f4aef9a91303c67eb6`

## TxGraffiti pin

- upstream: `RandyRDavila/TxGraffiti2`
- source revision/tag revision: `e37126da53b84150d142a5d61202b61f78521fcc`
- package: `txgraffiti==0.4.1`
- PyPI release date: 2026-01-07
- PyPI wheel SHA-256: `9b1b89742af8b180f0ece1c514b5c94a0d77580faeacdfcd7cd6b8c21aa33569`

## Calibration source checkpoint

`f0c42426fdabd3860837d3e3eb048a038842a655`

Successful CI run for that checkpoint: `36849930237`.

## Calibration hashes

- discovery corpus (orders 2–5, 7 unlabeled trees): `b0201c3e78452cf0544cba0e2f0922c2cb11309b78b2a8141e3881f93bc55656`
- untouched calibration holdout (order 6, 6 unlabeled trees): `00743205c74fb1257e408f7f99d63e354bdd5fc092209c3232b4a201914d4bad`

The only candidate created in TF0 is `TF-000001`, permanently marked `KNOWN_RESULT` / `KNOWN/CALIBRATION`. No research-discovery run was attempted.
