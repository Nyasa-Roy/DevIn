# Benchmarking

Run the local API benchmark from the repository root with `python tests/benchmark.py`. It measures 50 `/health` requests and reports average and p95 latency. Production benchmarking should additionally measure dashboard queries, sync duration, database query plans, and ML inference latency against representative repository fixtures.
