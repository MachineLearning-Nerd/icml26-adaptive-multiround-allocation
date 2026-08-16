#!/usr/bin/env python3
"""Fail-closed release verifier for the adaptive-allocation audit."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FINAL_REMOTE = "https://github.com/MachineLearning-Nerd/icml26-adaptive-multiround-allocation"
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
OFFICIAL_COMMIT = "5e174a13e35cf03c57167c7c333193bd48745a93"


def fail(message: str) -> None:
    raise SystemExit(f"VERIFY_FAIL: {message}")


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode:
        fail(f"command failed: {' '.join(args)}\n{result.stdout}{result.stderr}")
    return result.stdout.strip()


def require_files() -> None:
    required = [
        "README.md",
        "STATUS.md",
        "CLAIM_EVIDENCE.md",
        "SOURCE_MANIFEST.md",
        "BRANCH_AUDIT.md",
        "CITATION.cff",
        "requirements.txt",
        "docs/SOURCE_AUDIT.md",
        "repro/configs/full.json",
        "repro/src/run_allocation.py",
        "repro/tests/test_allocation.py",
        "outputs/dp_scaling.csv",
        "outputs/summary.json",
        "official/policies/our_policy.py",
        "official/core/population_distribution_object.py",
        "official/core/utils.py",
        "official/requirements.txt",
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")


def check_docs() -> None:
    readme = (ROOT / "README.md").read_text()
    evidence = (ROOT / "CLAIM_EVIDENCE.md").read_text()
    manifest = (ROOT / "SOURCE_MANIFEST.md").read_text()
    branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text()
    source_audit = (ROOT / "docs/SOURCE_AUDIT.md").read_text()
    citation = (ROOT / "CITATION.cff").read_text()
    for marker in (
        "Adaptive Multi-Round",
        "Stochastic Arrivals",
        "Yuqi Pan",
        "Cheryl Johnson",
        "NOT_REPRODUCED",
        "ICPSR",
        "Official implementation",
        "Thank you",
    ):
        if marker not in readme:
            fail(f"README is missing marker: {marker}")
    for marker in (
        "Claim 1",
        "Claim 2",
        "Claim 3",
        "exhaustive_greedy_check",
        "independent_population_dp",
        "NOT_REPRODUCED",
    ):
        if marker not in evidence:
            fail(f"claim evidence is missing marker: {marker}")
    for marker in ("official/", "run_allocation.py", OFFICIAL_COMMIT, "ICPSR"):
        if marker not in manifest or marker not in source_audit:
            fail(f"source provenance is missing marker: {marker}")
    for marker in ("main", "master", "`orx`", "Co-author trailers"):
        if marker not in branch_audit:
            fail(f"branch audit is missing marker: {marker}")
    for marker in ("repository-code:", "10.48550/arXiv.2605.12111", "Johnson"):
        if marker not in citation:
            fail(f"citation file is missing marker: {marker}")
    if (ROOT / "requirements.txt").read_text().splitlines() != [
        "numpy==2.3.1",
        "pytest==8.4.1",
    ]:
        fail("requirements.txt is not pinned to the audited environment")


def check_git_state() -> None:
    if run("git", "branch", "--show-current") != "main":
        fail("current branch is not main")
    remote = run("git", "remote", "get-url", "origin").removesuffix(".git")
    if remote != FINAL_REMOTE:
        fail(f"origin is {remote!r}, expected {FINAL_REMOTE!r}")
    if run("git", "status", "--porcelain"):
        fail("working tree is not clean")
    refs = run("git", "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes").splitlines()
    if any(ref.endswith("/master") or ref.endswith("/orx") for ref in refs):
        fail(f"retired/generated branch remains: {refs}")
    if "refs/heads/main" not in refs:
        fail("refs/heads/main is missing")
    if any("repro-HigEPnWgLQ" in ref for ref in refs):
        fail(f"old repository slug remains in refs: {refs}")
    records = run("git", "log", "--all", "--format=%H%x00%an%x00%ae%x00%cn%x00%ce").splitlines()
    if not records:
        fail("no reachable commits")
    for record in records:
        fields = record.split("\x00")
        if len(fields) != 5:
            fail(f"malformed commit record: {record}")
        _, author, author_email, committer, committer_email = fields
        if (author, author_email, committer, committer_email) != (
            CANONICAL_NAME,
            CANONICAL_EMAIL,
            CANONICAL_NAME,
            CANONICAL_EMAIL,
        ):
            fail(f"non-canonical commit identity: {record}")
    messages = run("git", "log", "--all", "--format=%B")
    if any(line.lower().startswith("co-authored-by:") for line in messages.splitlines()):
        fail("a reachable commit contains a co-author trailer")


def rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="") as handle:
        return list(csv.DictReader(handle))


def check_outputs() -> None:
    data = json.loads((ROOT / "outputs/summary.json").read_text())
    c1 = data["claim1_greedy_optimality"]
    c2 = data["claim2_population_dp"]
    c3 = data["claim3_robustness"]
    if (c1["frontier_budget_cases"], c1["allocations_enumerated"]) != (1881, 72609):
        fail(f"C1 coverage changed: {c1}")
    if c1["max_oracle_gap"] >= 1e-12 or c1["max_marginal_identity_error"] >= 1e-12:
        fail(f"C1 numerical threshold failed: {c1}")
    if (c2["largest_budget"], len(c2["rows"])) != (20, 7):
        fail(f"C2 coverage changed: {c2}")
    if c2["max_state_error"] >= 1e-12:
        fail(f"C2 numerical threshold failed: {c2}")
    if c3["single_round"]["random_cases"] != 1500:
        fail(f"single-round case count changed: {c3}")
    if c3["single_round"]["max_bound_violation"] > 1e-12 or c3["single_round"]["max_tightness_error"] > 1e-12:
        fail(f"single-round robustness threshold failed: {c3}")
    multi = c3["multi_round"]
    if set(multi["cases"]) != {"heterogeneous_exact_models", "homogeneous_zero_bound", "noisy_models"}:
        fail(f"multi-round cases changed: {multi}")
    if multi["max_bound_violation"] > 1e-12:
        fail(f"multi-round bound threshold failed: {multi}")
    noisy = multi["cases"]["noisy_models"]
    homogeneous = multi["cases"]["homogeneous_zero_bound"]
    if noisy["lhs_suboptimality"] <= 0.1 or noisy["lhs_suboptimality"] > noisy["rhs_bound"] + 1e-12:
        fail(f"noisy multi-round control changed: {noisy}")
    if homogeneous["lhs_suboptimality"] != 0.0 or homogeneous["rhs_bound"] != 0.0:
        fail(f"homogeneous zero-bound control changed: {homogeneous}")
    dp_rows = rows("outputs/dp_scaling.csv")
    if len(dp_rows) != 7 or max(float(row["max_state_error"]) for row in dp_rows) >= 1e-12:
        fail("DP CSV does not match the audited seven-row run")


def check_tests() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = f"{result.stdout}\n{result.stderr}"
    if result.returncode:
        fail(f"focused tests failed:\n{output}")
    if "19 passed" not in output:
        fail(f"focused test count changed:\n{output}")


def main() -> None:
    require_files()
    check_docs()
    check_git_state()
    check_outputs()
    check_tests()
    print("FINAL_VERIFICATION_PASS")
    print(f"repository={FINAL_REMOTE}")
    print("branch=main")
    print(f"reachable_commits={len(run('git', 'rev-list', '--all').splitlines())}")
    print("commit_identity=canonical")
    print("claim_boundaries=PASS")
    print("focused_tests=PASS")


if __name__ == "__main__":
    main()
