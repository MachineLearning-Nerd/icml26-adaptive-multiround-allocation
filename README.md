# icml26-adaptive-multiround-allocation

Independent evidence audit and finite reproduction for **Adaptive Multi-Round
Allocation with Stochastic Arrivals**.

## Paper

- **Authors:** Yuqi Pan, Davin Choo, Haichuan Wang, Milind Tambe, Alastair van
  Heerden, and Cheryl Johnson
- **Paper:** [arXiv:2605.12111v2](https://arxiv.org/abs/2605.12111) (accepted
  to ICML 2026; current arXiv version 20 July 2026)
- **OpenReview:** [HigEPnWgLQ](https://openreview.net/forum?id=HigEPnWgLQ)
- **Canonical repository:**
  <https://github.com/MachineLearning-Nerd/icml26-adaptive-multiround-allocation>
- **Official implementation snapshot:**
  [`cxjdavin/Adaptive-Multi-Round-Allocation-with-Stochastic-Arrivals`](https://github.com/cxjdavin/Adaptive-Multi-Round-Allocation-with-Stochastic-Arrivals)
  at commit `5e174a13e35cf03c57167c7c333193bd48745a93`

The paper models sequential resource allocation where each allocated unit can
produce stochastic referrals and therefore change the next round's frontier.
It combines exact greedy allocation within a round with a population-level
surrogate dynamic program for planning across rounds, then analyzes model
misspecification.

## Reproduction status

The statuses below describe the evidence in this repository. Finite numerical
checks support the stated scope; they are not replacements for the paper's
general proofs.

| Paper result | Status | Evidence boundary |
|---|---|---|
| Theorem 4.2: greedy allocation is optimal for a realized single-round frontier | `SUPPORTED_FINITE_EXHAUSTIVE` | 1,881 frontier/budget cases and 72,609 integer allocations, checked against an independent composition enumerator |
| Proposition 6.1 / surrogate transition construction | `SUPPORTED_IMPLEMENTATION_REPLAY` | The unchanged official even-allocation/PGF path is compared with direct-convolution transitions on an exact finite population mixture |
| Theorem 6.2: polynomial population-level DP | `SUPPORTED_FINITE_SCALING` | Seven budgets through `b=20`, all `441` states at the largest budget, and an independent Bellman recursion; asymptotic complexity remains a theorem-level claim |
| Proposition 7.1: tight single-round robustness bound | `SUPPORTED_FINITE_TIGHTNESS` | 1,500 seeded noisy-frontier cases plus six adversarial equality constructions |
| Theorem 7.2: three-term multi-round robustness decomposition | `SUPPORTED_FINITE_MODEL_CHECKS` | Exact finite multi-round MDP checks for homogeneous, heterogeneous, and noisy models; the oracle is scoped to the paper's greedy-within-round policy family |
| ICPSR network experiments and all paper figures/tables | `NOT_REPRODUCED` | The external ICPSR 22140 data are not downloaded; vendored official figures are provenance artifacts, not regenerated results |

## What is in the repository

There are two deliberately separate code paths:

- [`official/`](official/) is a vendored snapshot of the authors' implementation
  at the commit above. The reproduction imports the official
  `OurPolicy.greedy_single_stage`, `precompute_surrogate`, and population/PGF
  utilities without modifying their algorithmic code.
- [`repro/src/run_allocation.py`](repro/src/run_allocation.py) is the audit
  harness. It supplies exact finite distributions, independent oracles,
  exhaustive checks, and the stored evidence producer.

The main paths are:

| Claim | Producer path | Independent reference |
|---|---|---|
| Single-round greedy optimality | `exhaustive_greedy_check` → official `OurPolicy.greedy_single_stage` | `compositions` + direct expected reward and PMF enumeration |
| Population DP agreement | `dp_check` → official `precompute_surrogate` | `independent_population_dp` + `truncated_pmf`/`convolve_many` |
| Single-round robustness | `single_round_robustness` | seeded random frontiers and an explicit tied adversarial family |
| Multi-round bound | `exact_multiround_case` / `multi_round_robustness` | exact distribution-valued frontier recursion and independent transition convolution |

The exact finite mixture in the DP check cycles through two PMFs. Because the
official code requests exactly 1,200 samples, the cycle is balanced and the
population mixture passed to the official surrogate is exact rather than a
Monte Carlo approximation.

## Committed results

- **Greedy:** all `1,881` cases match exhaustive optimization; maximum objective
  gap `8.881784197001252e-16`; maximum marginal-identity error
  `8.881784197001252e-16`.
- **Population DP:** official and independent tables agree through `b=20`;
  maximum state error `1.7763568394002505e-15`; the largest row checks `441`
  states and `4,600` action evaluations.
- **Single-round robustness:** no bound violation in `1,500` random cases;
  six tight cases through budget `13`; maximum tightness error
  `2.6645352591003757e-15`.
- **Multi-round robustness:** the recorded noisy case has suboptimality
  `0.38910442372275034` against a bound of `49.8331641754494`; the homogeneous
  control has zero suboptimality and zero bound; maximum recorded bound
  violation is `0.0`.

The canonical aggregate is [`outputs/summary.json`](outputs/summary.json), and
the DP table is [`outputs/dp_scaling.csv`](outputs/dp_scaling.csv).

## Reproduce the audit

The focused audit needs Python 3.11+ and the pinned dependencies in
[`requirements.txt`](requirements.txt):

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

python -m pytest -q
python repro/src/run_allocation.py \
  --config repro/configs/full.json \
  --output-dir outputs

# Final release gate; checks the published repository state as well as claims.
python verify_final.py
```

The official experiment runner in `official/run_experiments.py` requires the
external ICPSR data and is intentionally not part of the release gate. Its
additional dependencies are listed separately in
[`official/requirements.txt`](official/requirements.txt).

## Citation and thanks

Please cite both the original paper and this audit when using the repository.
[`CITATION.cff`](CITATION.cff) contains machine-readable metadata.

Thank you to Yuqi Pan, Davin Choo, Haichuan Wang, Milind Tambe, Alastair van
Heerden, and Cheryl Johnson for the clear model, exact greedy/PGF construction,
and robustness analysis, and for releasing an implementation that makes an
independent audit possible. This repository is independent and is not an
author-endorsed or official release.

All publication commits are attributed to `MachineLearning-Nerd`.
