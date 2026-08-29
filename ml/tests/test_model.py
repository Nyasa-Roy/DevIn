from ml.dataset import build_dataset
from ml.model import evaluate, train_baseline


def test_baseline_trains_and_reports_classification_metrics() -> None:
    records = [{"lines_added": size, "files_changed": size // 10, "reverted": size > 100} for size in [1, 5, 10, 120, 180, 250]]
    rows = build_dataset(records)
    model = train_baseline(rows)
    metrics = evaluate(model, rows)
    assert {"precision", "recall", "f1", "pr_auc", "roc_auc"} <= metrics.keys()
    assert 0 <= metrics["f1"] <= 1
