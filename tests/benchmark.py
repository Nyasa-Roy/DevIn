"""Small repeatable local API benchmark for Phase 14."""

import statistics
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parents[1] / "backend"))
from app.main import app


def main() -> None:
    samples = []
    with TestClient(app) as client:
        for _ in range(50):
            start = time.perf_counter()
            response = client.get("/health")
            response.raise_for_status()
            samples.append((time.perf_counter() - start) * 1000)
    ordered = sorted(samples)
    print({"requests": len(samples), "average_ms": round(statistics.mean(samples), 2), "p95_ms": round(ordered[round(len(ordered) * 0.95) - 1], 2)})


if __name__ == "__main__":
    main()
