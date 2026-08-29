from sklearn.ensemble import IsolationForest


def detect_anomalies(values: list[dict], contamination: float = 0.1) -> list[dict]:
    if len(values) < 4:
        return []
    features = [[float(item.get("lines_changed", 0)), float(item.get("files_changed", 0)), float(item.get("commits", 0))] for item in values]
    model = IsolationForest(contamination=min(contamination, 0.49), random_state=42)
    labels = model.fit_predict(features)
    scores = model.decision_function(features)
    return [{**item, "anomaly": label == -1, "anomaly_score": round(float(-score), 4)} for item, label, score in zip(values, labels, scores)]
