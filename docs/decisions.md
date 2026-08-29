# Architecture decisions

## ADR-001: PostgreSQL is the system of record

PostgreSQL provides transactions, mature relational querying, and a straightforward path to pgvector for semantic search. SQLite is supported only as a local test adapter.

## ADR-002: FastAPI is the backend boundary

FastAPI provides typed request/response contracts, async-friendly endpoints, and generated OpenAPI documentation while keeping Python close to the data and ML layers.
