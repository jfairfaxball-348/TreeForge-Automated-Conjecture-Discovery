# Project charter

## Mission

Build a rigorous experimental system capable of finding a small number of mathematically meaningful conjectures about finite trees that survive increasingly hostile scrutiny and can later become standalone theorem projects.

## Initial universe

Finite, simple, unlabeled trees. Tree isomorphism is handled by an exact AHU-style canonical code, and corpus generation uses one representative of each unlabeled isomorphism class.

## Separation of concerns

TreeForge owns: corpus generation, invariant definitions and computation, conjecturing adapters, candidate identity, evidence, falsification, interpretation notes, provenance, and bounded novelty-audit records.

A graduated theorem repository owns: a frozen exact statement, proof development, Lean formalisation where appropriate, Palomar packaging where appropriate, paper preparation, arXiv packaging, and publication workflow.

## Non-goals

TreeForge does not seek maximal conjecture volume, does not convert numerical survival into theorem status, does not reopen completed predecessor projects merely to mine them, and does not treat automated conjecturing output as mathematical judgment.
