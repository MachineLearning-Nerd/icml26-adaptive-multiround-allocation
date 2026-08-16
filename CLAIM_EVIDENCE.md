# Claim-to-evidence audit

This file maps each reproduced paper result to the code that produces it, the
stored artifact, and the boundary of the evidence.

## Claim 1 — exact single-round greedy allocation

### Paper statement

For a realized frontier and fixed round budget, the expected reward decomposes
into survival-probability marginals. The paper's Theorem 4.2 states that taking
the largest currently available marginal at each step is optimal.

### Production path

1. `repro/src/run_allocation.py:exhaustive_greedy_check` enumerates frontier
   sizes 1–4, multisets from a six-PMF library, and budgets 0–8.
2. `official/policies/our_policy.py:OurPolicy.greedy_single_stage` supplies the
   policy under audit.
3. `repro/src/run_allocation.py:expected_reward` computes the objective from
   survival tails, while `compositions` enumerates every feasible integer
   allocation.
4. Each direct value is also checked against independent PMF enumeration of
   `E[min(k, X)]`.

### Stored evidence

The aggregate is in `outputs/summary.json`:

- `1,881` frontier/budget cases;
- `72,609` allocations enumerated;
- maximum greedy-to-oracle objective gap
  `8.881784197001252e-16`;
- maximum marginal-identity error
  `8.881784197001252e-16`.

This is `SUPPORTED_FINITE_EXHAUSTIVE`, not a replacement for the theorem's
universal proof.

## Claim 2 — population-level PGF dynamic program

### Paper statement

The population-level surrogate depends on remaining budget and frontier size.
Even allocation induces a truncated-PGF transition, and Theorem 6.2 gives an
`O(b^2)` table with `O(b^5 log b)` computation for total budget `b`.

### Production path

1. `repro/src/run_allocation.py:dp_check` creates two exact PMFs and a balanced
   `CyclingPopulation` with 1,200 samples.
2. `official/policies/our_policy.py:precompute_surrogate` produces the official
   surrogate table using the vendored PGF implementation.
3. `repro/src/run_allocation.py:independent_population_dp` computes the same
   Bellman recursion using `truncated_pmf` and `convolve_many`, without the
   official PGF utilities.
4. `outputs/dp_scaling.csv` records seven budgets `[4, 6, 8, 10, 12, 16, 20]`,
   state counts, action-loop counts, and maximum state errors.

### Stored evidence and boundary

The largest row checks 441 states and 4,600 action evaluations. The maximum
state error across all rows is `1.7763568394002505e-15`. This supports exact
finite agreement and the observed state/loop structure. It does not by itself
prove the asymptotic `O(b^5 log b)` theorem, nor does it independently re-prove
the even-allocation proposition in all distributions.

## Claim 3 — robustness decomposition

### Single-round path

`single_round_robustness` generates 1,500 seeded pairs of true/estimated PMFs,
compares the official greedy choices, and checks the total survival-tail error
bound. It then uses six explicit tied constructions at budgets
`1, 2, 3, 5, 8, 13` to test tightness. The maximum random bound violation is
`-0.004627134808053962`, and the maximum tightness error is
`2.6645352591003757e-15`.

### Multi-round path

`exact_multiround_case` builds exact frontier-size transition distributions and
solves the finite distribution-valued recursion with independent convolution.
`multi_round_robustness` records:

- `heterogeneous_exact_models`: exact model, positive finite suboptimality;
- `homogeneous_zero_bound`: zero heterogeneity, zero loss, zero bound;
- `noisy_models`: suboptimality `0.38910442372275034`, bound
  `49.8331641754494`.

The maximum recorded bound violation is `0.0`. The oracle is deliberately
scoped to the paper's implemented greedy-within-round policy family; it is not
an unrestricted arbitrary-allocation solver. These checks are
`SUPPORTED_FINITE_MODEL_CHECKS`, not an independent proof of Theorem 7.2.

## Tests and controls

`repro/tests/test_allocation.py` contains 19 focused tests covering:

- official greedy vs exhaustive allocation;
- marginal and truncated-PMF identities;
- direct convolution vs enumeration;
- DP boundaries and finite values;
- robustness and tightness;
- homogeneous zero-bound and noisy positive-loss controls;
- invalid-PMF and non-monotone-tail rejection controls;
- persisted summary thresholds.

## Not reproduced

The ICPSR 22140 empirical network experiment, external data download, all
official figure regeneration, and any claim not represented by the finite paths
above are intentionally `NOT_REPRODUCED`.
