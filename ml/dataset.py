import argparse
import csv
import json
from pathlib import Path

FEATURE_COLUMNS = ["lines_added", "lines_deleted", "lines_changed", "files_changed", "commits", "reviews", "author_previous_prs", "author_previous_reverts", "test_files_changed", "historical_file_churn"]


def risk_label(pr: dict) -> int:
    return int(bool(pr.get("reverted") or pr.get("bug_related_issue") or pr.get("follow_up_fixes", 0) >= 2))


def feature_row(pr: dict) -> dict:
    added, deleted = int(pr.get("lines_added", 0)), int(pr.get("lines_deleted", 0))
    return {"lines_added": added, "lines_deleted": deleted, "lines_changed": added + deleted, "files_changed": int(pr.get("files_changed", 0)), "commits": int(pr.get("commits", 0)), "reviews": int(pr.get("reviews", 0)), "author_previous_prs": int(pr.get("author_previous_prs", 0)), "author_previous_reverts": int(pr.get("author_previous_reverts", 0)), "test_files_changed": int(pr.get("test_files_changed", 0)), "historical_file_churn": float(pr.get("historical_file_churn", 0)), "risky": risk_label(pr)}


def build_dataset(records: list[dict]) -> list[dict]:
    return [feature_row(record) for record in records]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the DevInsight PR-risk training dataset")
    parser.add_argument("--input", type=Path, required=True, help="Input JSONL file")
    parser.add_argument("--output", type=Path, required=True, help="Output CSV file")
    args = parser.parse_args()
    records = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows = build_dataset(records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FEATURE_COLUMNS + ["risky"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
