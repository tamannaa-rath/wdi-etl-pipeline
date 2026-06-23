# Engineering Decisions Log

Short, dated entries. Each one: what was considered, what was decided, why. This is the proof of engineering judgment that a finished schema alone doesn't show.

---

**2026-06 — Dataset format discovery**
Initial plan assumed a wide-format `WDIData.csv` (`Country, 1960, 1961, ... 2025`) requiring a melt/unpivot step. Actual file obtained from World Bank Databank is an SDMX-style long-format export (`WB_WDI.csv`, 41 columns) — already one row per observation. Melt step is unnecessary. Real work shifted to column pruning and dimension design instead of reshaping.

**2026-06 — Breakdown dimensions: model or ignore?**
Dataset includes `SEX`, `AGE`, `URBANISATION` breakdown columns not present in the plain WDI wide CSV. Considered filtering to `_T` (Total) only to match the original simpler plan. Decided to model all three as real dimensions instead — more realistic star schema, better interview story, and the cardinality check (below) confirmed they carry real variation.

**2026-06 — Cardinality check methodology**
Sampled 50,000 rows from two non-overlapping sections of the 8.9M-row file (rows 0–50k, rows 4,000,000–4,050,000) and counted distinct values per candidate column. Rationale: a single sample from the start of a file can miss variation that appears later (e.g. different indicators or regions using different status codes). Two samples ~4M rows apart gives reasonable confidence a "constant" column is actually constant, without needing to scan all 8.9M rows up front.

**2026-06 — Final dimension list locked**
Based on the cardinality check: `SEX` (3 values), `AGE` (22 values), `URBANISATION` (3 values) confirmed as real dimensions. `OBS_STATUS`, `COMP_BREAKDOWN_1/2/3`, `FREQ` confirmed constant across both samples — dropped. Full reasoning per column in `DATA_DICTIONARY.md`. Final schema: 5 dimensions (`dim_country`, `dim_indicator`, `dim_date`, `dim_sex`, `dim_age`, `dim_urbanisation`) + 1 fact (`fact_wdi_data`).

**2026-06 — Fact table grain consequence**
Locking in 5 foreign keys on the fact table means a single (country, indicator, year) combination can have multiple rows — one for each sex/age/urbanisation breakdown present for that indicator. Flagged explicitly so the "simple lookup" success criterion (e.g. India's GDP per capita in 2020) is queried correctly with `WHERE sex_id = <Total> AND age_id = <Total> AND urban_id = <Total>`, not assumed to return one row by default.

**2026-06 — Project scope expansion**
Originally scoped as a local-only Phase 1 (no cloud, per the 3-phase roadmap). Team decision: pull forward Supabase (Gold layer hosting), Streamlit (public dashboard), self-hosted GitHub Actions runner, and daily cron scheduling into the current build, ahead of the original phase boundary. Tradeoff acknowledged: more infrastructure to learn before the core ETL/schema work is proven out, in exchange for a more complete end-to-end project sooner.

---

*New entries go at the bottom, dated, in the same short format: what was considered → what was decided → why.*