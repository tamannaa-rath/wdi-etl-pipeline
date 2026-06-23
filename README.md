# WDI Global Development ETL Pipeline

A production-style ETL pipeline that ingests the World Bank's World Development Indicators (WDI) dataset — 8.9M rows, 3.6GB, SDMX format — cleans it, models it into a star schema, and serves it for analysis.

## Business Problem

> An NGO wants to analyze the relationship between a country's GDP growth and life expectancy over the last 20 years to prioritize development funding.

This pipeline makes that kind of cross-country, cross-indicator, time-series analysis queryable in seconds instead of requiring manual spreadsheet work across a 3.6GB raw export.

## Dataset

- **Source:** World Bank Databank — World Development Indicators (SDMX export)
- **Size:** 8,894,932 rows × 41 columns, 3.6GB
- **Format:** Long format (one row per observation) — not the classic wide `Country, 1960...2025` CSV
- **Breakdowns:** Indicators can be split by Sex (Total/Male/Female), Age (22 bands), and Urbanisation (Total/Rural/Urban)

See [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) for the full column-by-column breakdown of what was kept, what was dropped, and why.

## Architecture

```
Raw CSV (Bronze)  →  Chunked Extract + Clean  →  Star Schema (Silver, local Postgres)  →  Aggregates (Gold, cloud)  →  Dashboard
```

Full diagram and reasoning: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) *(in progress)*

## Star Schema

5 dimension tables + 1 fact table. Full design rationale: [`docs/DESIGN.md`](docs/DESIGN.md) *(in progress)*

```
dim_country        dim_indicator        dim_date
dim_sex            dim_age              dim_urbanisation
                        ↓
                  fact_wdi_data
```

## Tech Stack

| Category | Tool | Why |
|---|---|---|
| Package management | `uv` | Fast, reproducible, lockfile-based |
| Language | Python 3.10+ | pandas + sqlalchemy for chunked processing |
| Processing | pandas (chunked) | 3.6GB file, can't load in one shot |
| Database (Silver) | PostgreSQL via Docker | Local, free, full control |
| Database (Gold) | Supabase | Cloud-hosted aggregates for public serving |
| Orchestration | Bash + GitHub Actions | Local script + CI on push |
| Testing | pytest | Data quality checks (nulls, row counts, grain) |
| Dashboard | Streamlit | Public-facing view of Gold tables |

## Project Structure

```
wdi-etl-pipeline/
├── docs/                  # Data dictionary, design rationale, architecture, decisions log
├── data/
│   ├── raw/               # Full WB_WDI.csv (gitignored — too large for git)
│   └── samples/           # Small CSV slices for local dev without the full file
├── sql/
│   └── schema.sql         # CREATE TABLE statements for the star schema
├── scripts/
│   ├── extract.py
│   ├── clean.py
│   ├── load.py
│   └── run_pipeline.sh
├── tests/
│   └── test_data_quality.py
└── .github/workflows/
    └── pipeline.yml
```

## Quickstart

```bash
# Install dependencies
uv sync

# Start local Postgres
docker compose up -d

# Run the full pipeline
./scripts/run_pipeline.sh

# Run tests
uv run pytest tests/
```

## Status

🚧 Schema locked. Pipeline scripts in progress. See [`docs/DECISIONS.md`](docs/DECISIONS.md) for the engineering log.

## Team

Built by a 2-person team as a portfolio / learning project. Task ownership and sprint breakdown to be added as the build progresses.