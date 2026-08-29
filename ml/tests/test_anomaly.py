from ml.anomaly import detect_anomalies


def test_isolation_forest_marks_outlier() -> None:
    values = [{"lines_changed": value, "files_changed": 1, "commits": 1} for value in [10, 11, 9, 12, 5000]]
    results = detect_anomalies(values)
    assert any(item["anomaly"] for item in results)
