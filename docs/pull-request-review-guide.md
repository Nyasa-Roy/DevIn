# Pull request review guide

Use DevInsight's pull-request risk score to decide where review time is most useful.

## Review workflow

1. Synchronise the connected repository.
2. Open the repository overview in DevInsight.
3. Find the pull request in the **Pull request analysis** section.
4. Read the risk percentage and the factors that contributed to it.
5. Use the score to prioritise review; do not treat it as proof of a defect.

## Interpreting the score

- **Low risk:** a small change surface with few warning signals.
- **Medium risk:** review the change size and available coverage before merging.
- **High risk:** prioritise deeper review and additional validation.

The current baseline considers changed lines, changed files, and review coverage. Future versions can add test results, ownership context, and historical defect labels.
