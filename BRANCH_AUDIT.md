# Branch and history audit

## Required final state

| Item | Required state |
|---|---|
| Repository | `MachineLearning-Nerd/icml26-adaptive-multiround-allocation` |
| Default branch | `main` |
| Published branches | exactly `main` |
| Retired/generated branches | no `master`, `orx`, or session-specific branch |
| Commit author and committer | `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>` |
| Co-author trailers | none |

The current repository already uses `main`; the publication migration still
normalizes all reachable commit identities and removes any legacy remote refs.
The branch is the paper release path, not a claim-specific experiment branch.

## Verification

```bash
python verify_final.py
```

The verifier checks the local refs, final `origin` URL, canonical identities,
absence of co-author trailers, required documentation, committed metrics,
working-tree cleanliness, and 19 focused tests. The final GitHub API branch
list, default branch, tip, and remote commit identities are checked during
publication and recorded in the collection tracker.
