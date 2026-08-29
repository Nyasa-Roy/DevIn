# DevInsight ML

## Phase 8 dataset contract

`dataset.py` converts historical pull-request records into deterministic training rows. A PR is labelled risky (`1`) when its history indicates a revert, a bug-related issue, or significant follow-up fixes. This label is an operational assessment for model training, not a claim that the PR caused a defect.

Example:

```powershell
python ml/dataset.py --input ml/data/pull_requests.jsonl --output ml/data/pr_training.csv
```
