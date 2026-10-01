# TF1 cost benchmark

Benchmark date: 2026-10-01. The benchmark used the TF0 invariant algorithms at repository HEAD `f6c351b4a7a94941ab524bdfb9ec599409abcb2a`, Python 3.13.5, NetworkX 3.6.1, on the current execution host. Timings are wall-clock seconds and are intended only to choose conservative census bounds; they are not performance guarantees.

Command represented by the committed benchmark harness:

```bash
python experiments/benchmark_tf1.py --output experiments/TF1_BENCHMARK.json
```

| order | unlabeled trees | generation | core structural pass | domination | maximal-IS count | TreeStack estimate |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | 23 | 0.0031 | 0.0025 | 0.0006 | 0.0133 | 0.0015 |
| 9 | 47 | 0.0052 | 0.0058 | 0.0028 | 0.0520 | 0.0039 |
| 10 | 106 | 0.0108 | 0.0146 | 0.0113 | 0.2662 | 0.0103 |
| 11 | 235 | 0.0276 | 0.0380 | 0.0588 | 1.1809 | 0.0314 |
| 12 | 551 | 0.0646 | 0.1027 | 0.2996 | 5.6285 | 0.0760 |

Optional predecessor-inspired quantities were measured separately rather than mixed into the first discovery feature set. Exact ProbStack finite probabilities over all trees took about 0.0024/0.0147/0.0638 seconds at order 6 for totals 2/4/6, and about 0.0089/0.1709/0.2536 seconds at order 7. Exact Greedy-Uniformity bias over all trees took about 0.0115 seconds at order 6, 0.1257 seconds at order 7, and 2.3721 seconds at order 8.

The sharp increase in permutation enumeration and maximal-independent-set enumeration is the reason TF1 does not use those optional quantities indiscriminately or enlarge the census just because unlabeled-tree generation itself remains cheap.

Decision: freeze discovery at orders 2–10 and untouched holdout at order 11. The first controlled run uses only core exact invariants.
