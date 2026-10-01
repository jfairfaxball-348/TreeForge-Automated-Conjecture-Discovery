# TF1 cost benchmark

TF1 used two benchmark passes: a local pre-freeze measurement to choose conservative bounds, followed by a reproducibility confirmation in GitHub Actions before the successful controlled run.

The committed harness is:

```bash
python experiments/benchmark_tf1.py --output experiments/TF1-0001/benchmark_ci.json
```

The successful CI confirmation ran under Python 3.11.16 with NetworkX 3.6.1. Wall-clock seconds were:

| order | unlabeled trees | generation | core structural pass | domination | maximal-IS count | TreeStack estimate |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | 23 | 0.0065 | 0.0046 | 0.0009 | 0.0229 | 0.0024 |
| 9 | 47 | 0.0077 | 0.0087 | 0.0038 | 0.0937 | 0.0057 |
| 10 | 106 | 0.0181 | 0.0224 | 0.0172 | 0.4150 | 0.0155 |
| 11 | 235 | 0.0530 | 0.0582 | 0.0748 | 1.8659 | 0.0400 |
| 12 | 551 | 0.1166 | 0.1503 | 0.3525 | 8.8156 | 0.1088 |

Optional predecessor-inspired quantities were benchmarked separately. On paths, exact ProbStack finite probabilities at totals 2/4/6 took about 0.0009/0.0053/0.0194 seconds at order 6 and 0.0017/0.0120/0.0522 seconds at order 7. Exact Greedy-Uniformity bias took about 0.0027 seconds at order 6, 0.0197 seconds at order 7, and 0.1771 seconds at order 8.

The key observation is that unlabeled-tree generation remains cheap while exhaustive combinatorial invariants grow materially faster. This justified the pre-frozen choice of discovery orders 2–10 and untouched holdout order 11, and it justified keeping optional predecessor-inspired quantities out of the first discovery feature set.

The exact CI timing artifact is `experiments/TF1-0001/benchmark_ci.json`.
