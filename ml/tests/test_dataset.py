from ml.dataset import build_dataset


def test_dataset_features_and_label_are_deterministic() -> None:
    rows = build_dataset([{"lines_added": 10, "lines_deleted": 4, "files_changed": 2, "commits": 3, "reviews": 1, "follow_up_fixes": 2}])
    assert rows == [{"lines_added": 10, "lines_deleted": 4, "lines_changed": 14, "files_changed": 2, "commits": 3, "reviews": 1, "author_previous_prs": 0, "author_previous_reverts": 0, "test_files_changed": 0, "historical_file_churn": 0.0, "risky": 1}]


def test_clean_pr_is_not_risky() -> None:
    assert build_dataset([{"lines_added": 1}])[0]["risky"] == 0
