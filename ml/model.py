import argparse
import csv
from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml.dataset import FEATURE_COLUMNS


def train_baseline(rows: list[dict]) -> Pipeline:
    x = [[float(row[column]) for column in FEATURE_COLUMNS] for row in rows]
    y = [int(row["risky"]) for row in rows]
    model = Pipeline([("scale", StandardScaler()), ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    model.fit(x, y)
    return model


def evaluate(model: Pipeline, rows: list[dict]) -> dict[str, float]:
    x = [[float(row[column]) for column in FEATURE_COLUMNS] for row in rows]
    y = [int(row["risky"]) for row in rows]
    probabilities = model.predict_proba(x)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    metrics = {"precision": precision_score(y, predictions, zero_division=0), "recall": recall_score(y, predictions, zero_division=0), "f1": f1_score(y, predictions, zero_division=0), "pr_auc": average_precision_score(y, probabilities)}
    if len(set(y)) > 1:
        metrics["roc_auc"] = roc_auc_score(y, probabilities)
    return {key: round(float(value), 4) for key, value in metrics.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the DevInsight baseline PR risk model")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    args = parser.parse_args()
    with args.input.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    model = train_baseline(rows)
    args.model.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model)
    print(evaluate(model, rows))


if __name__ == "__main__":
    main()
