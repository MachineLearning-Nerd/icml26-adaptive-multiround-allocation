# Status — icml26-adaptive-multiround-allocation

**Paper:** *Adaptive Multi-Round Allocation with Stochastic Arrivals*
**Authors:** Yuqi Pan, Davin Choo, Haichuan Wang, Milind Tambe, Alastair van
Heerden, and Cheryl Johnson
**Sources:** [arXiv:2605.12111v2](https://arxiv.org/abs/2605.12111) ·
[OpenReview HigEPnWgLQ](https://openreview.net/forum?id=HigEPnWgLQ)

## Release state

The finite, paper-scoped reproduction and evidence documentation are complete.
The final remote-state gate is repeatable with `verify_final.py`: it checks the
canonical repository URL, one `main` branch, commit attribution, the stored
metrics, and the focused tests from a fresh clone.

## Evidence

- The official greedy policy matches an independent exhaustive oracle in 1,881
  frontier/budget cases over 72,609 allocations.
- The official population-level PGF DP agrees with an independently implemented
  direct-convolution Bellman recursion through budget 20, with maximum state
  error `1.7763568394002505e-15`.
- Proposition 7.1 is checked with 1,500 noisy cases and six exact equality
  constructions; the maximum equality error is `2.6645352591003757e-15`.
- The multi-round decomposition is checked on homogeneous, heterogeneous, and
  noisy finite models, including zero-bound and positive-suboptimality controls.
- The focused suite reports 19 passing tests.

## Explicit limits

- The checks support finite instances and implementation paths; they do not
  independently prove Theorem 4.2, Proposition 6.1, Theorem 6.2, Proposition
  7.1, or Theorem 7.2 for all admissible distributions.
- The multi-round oracle compares policies within the implemented
  greedy-within-round family, not an unrestricted arbitrary-allocation Bellman
  solver.
- The ICPSR 22140 network experiment, external data download, and complete
  paper figures/tables are `NOT_REPRODUCED`.

## Provenance

The official snapshot is pinned to
`cxjdavin/Adaptive-Multi-Round-Allocation-with-Stochastic-Arrivals` commit
`5e174a13e35cf03c57167c7c333193bd48745a93`. The independent oracles and audit
paths are in [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md); file-level provenance is
in [`SOURCE_MANIFEST.md`](SOURCE_MANIFEST.md).
