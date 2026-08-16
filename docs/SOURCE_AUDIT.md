# Source audit

## Primary paper

- *Adaptive Multi-Round Allocation with Stochastic Arrivals*
- [arXiv:2605.12111v2](https://arxiv.org/abs/2605.12111), current version dated
  2026-07-20
- [OpenReview HigEPnWgLQ](https://openreview.net/forum?id=HigEPnWgLQ)
- Authors: Yuqi Pan, Davin Choo, Haichuan Wang, Milind Tambe, Alastair van
  Heerden, and Cheryl Johnson

The paper's abstract and Sections 4–7 define the results audited here:
single-round greedy allocation, a population-level surrogate with truncated
PGF transitions, and a three-term robustness analysis.

## Official implementation provenance

- Repository:
  `cxjdavin/Adaptive-Multi-Round-Allocation-with-Stochastic-Arrivals`
- Vendored commit: `5e174a13e35cf03c57167c7c333193bd48745a93`
- Official paths used by the harness:
  - `official/policies/our_policy.py`
  - `official/core/population_distribution_object.py`
  - `official/core/utils.py`

The official policy and surrogate code are retained under `official/`. The
reproduction harness imports those paths and does not silently replace their
algorithmic implementation. `repro/src/run_allocation.py` adds exact finite
distributions and independent oracles around them.

## Scope decision

The official project includes an ICPSR 22140 network experiment whose data are
external and whose execution requires the dataset download. The audit therefore
does not claim to reproduce that experiment. The checked-in official figures
are preserved as source artifacts only; they are not regenerated or treated as
independent evidence.

The finite population used in the DP audit cycles through two distribution types
and supplies exactly 1,200 samples. This makes the mixture passed into the
unchanged official DP exactly balanced, isolating algorithm agreement from
Monte Carlo sampling noise.
