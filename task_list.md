# Task List — WDI ETL Pipeline

How to use this file: check a box by changing `[ ]` to `[x]` when a task is done, then `git add task_list.md && git commit -m "..."` so your teammate sees it updated on pull. A phase should only start once the previous phase's boxes are all checked.

Progress: **0 / 10 phases complete**

---

## Phase 0 — Foundation
**Status:** ✅ Complete

- [x] **Cardinality check** — Owner: Himanshu — Sampled the 8.9M-row file at two points using pandas to test column variation. Goal: decide which columns become dimensions vs. get dropped.
- [x] **Star schema design** — Owner: Tamanna — Shaped the cardinality results into 5 dimension tables + 1 fact table. Goal: lock exact tables and foreign keys before writing code.

---

## Phase 1 — Extraction
**Status:** ✅ Complete

- [x] **Build `extract.py`** — Owner: Himanshu — Read the 3.6GB CSV in fixed-size chunks using pandas `read_csv(chunksize=...)`. Goal: make the full file readable without crashing memory.
- [x] **Verify row integrity** — Owner: Himanshu — Sum chunk row counts and compare against the `wc -l` total (8,894,932). Goal: confirm no rows silently dropped.

**Definition of Done:** Full file reads end-to-end, row count matches exactly.

**Study topic for Tamanna (while this runs):** pandas `dtype` parameter and why specifying types upfront avoids memory bloat; how chunked iteration works conceptually. (Prepares her to review this, and feeds directly into Phase 2.)

---

## Phase 2 — Cleaning & Transformation
**Status:** ⬜ Not Started

- [ ] **Drop constant columns** — Owner: Tamanna — Remove `FREQ`, `OBS_STATUS`, `COMP_BREAKDOWN_1/2/3`, and SDMX plumbing columns using pandas. Goal: reduce 41 columns to only what the schema needs.
- [ ] **Collapse label pairs** — Owner: Tamanna — Merge each `CODE`/`CODE_LABEL` pair into single lookup-ready fields. Goal: clean dimension source data, no duplicate columns.
- [ ] **Build `dim_age` parser** — Owner: Tamanna — Decode codes like `Y15T24` into readable labels ("15 to 24 years") using regex or a manual dict; handle `_T` and "and over" style codes. Goal: all 22 AGE codes decode correctly.
- [ ] **Null handling** — Owner: Tamanna — Drop/flag rows where `OBS_VALUE` is null using pandas. Goal: keep nulls under 1% in key columns.

**Definition of Done:** Output matches `docs/DATA_DICTIONARY.md` shapes exactly, all 22 AGE codes decode correctly, nulls under threshold.

**Study topic for Himanshu (while this runs):** SQLAlchemy ORM basics (`engine`, `Session`, `Base.metadata`), connection pooling concepts. (Direct prep for Phase 3 — loading what this phase produces.)

---

## Phase 3 — Loading
**Status:** ⬜ Not Started

- [ ] **Build dimension loaders** — Owner: Himanshu — Insert unique values into all 6 dimension tables using SQLAlchemy + psycopg2. Goal: every dimension table populated, no duplicates.
- [ ] **Build fact loader** — Owner: Himanshu — Resolve cleaned rows into foreign keys, insert into `fact_wdi_data`. Goal: every fact row correctly linked, no orphaned FKs.
- [ ] **Validation query** — Owner: Himanshu — Run the India-2020-GDP check filtered to Total/Total/Total using raw SQL. Goal: confirm grain is correct, exactly one row returned.

**Definition of Done:** All 6 tables populated, validation query returns exactly one row.

**Study topic for Tamanna (while this runs):** What a Docker container actually is (process isolation, image vs. container), Docker Compose YAML structure. (First new-territory topic — prep to participate in Phase 4, not own it solo yet.)

---

## Phase 4 — Local Infra & Automation
**Status:** ⬜ Not Started

- [ ] **Docker Compose setup** — Owner: Himanshu (Tamanna shadows hands-on, runs commands herself) — Define a Postgres service (image, ports, volume, env vars) in `docker-compose.yml`. Goal: one command spins up a working local database.
- [ ] **Build `run_pipeline.sh`** — Owner: Himanshu — Chain extract → clean → load into one executable Bash script. Goal: full pipeline runs end-to-end, under 2 minutes.

**Definition of Done:** `./run_pipeline.sh` works from a clean repo clone.

**Study topic for Tamanna (while this runs):** `pytest` fixtures, basic data-quality assertions (row counts, null checks, range checks). (Direct prep — she owns the next phase.)

---

## Phase 5 — Testing
**Status:** ⬜ Not Started

- [ ] **Write `test_data_quality.py`** — Owner: Tamanna — Assert row counts, null rates, duplicate checks, FK integrity using pytest. Goal: catch pipeline breakage automatically.
- [ ] **Test `dim_age` parser** — Owner: Tamanna — Unit test the age code parser for correctness and edge cases. Goal: prove the trickiest transformation logic works.

**Definition of Done:** All tests pass on a fresh pipeline run, consistently (no flaky tests).

**Study topic for Himanshu (while this runs):** GitHub Actions YAML syntax (`on: push`, `jobs:`, `steps:`), what a CI runner does. (Prep for Phase 6, which he leads.)

---

## Phase 6 — CI/CD
**Status:** ⬜ Not Started

- [ ] **Build `pipeline.yml` test trigger** — Owner: Himanshu — Run pytest automatically on every push using GitHub Actions. Goal: catch broken code before merge.
- [ ] **Build second trigger** — Owner: Himanshu & Tamanna (paired, written together) — Add a manual or scheduled trigger to re-run the pipeline.

**Definition of Done:** A push shows pass/fail status automatically in GitHub.

**Study topic for Tamanna (while this runs):** Streamlit basics (`st.dataframe`, `st.line_chart`, `st.selectbox`). (Direct prep for her piece of Phase 7.)

---

## Phase 7 — Cloud & Serving
**Status:** ⬜ Not Started

- [ ] **Supabase setup + Gold push** — Owner: Himanshu — Create aggregate tables (e.g. `gold_gdp_by_country`) and push to Supabase using SQLAlchemy. Goal: small, fast, cloud-hosted tables.
- [ ] **Streamlit dashboard** — Owner: Tamanna — Build charts for GDP per capita and life expectancy, filterable by country, reading from Supabase. Goal: a public URL anyone can explore.

**Definition of Done:** Public Streamlit URL shows working, live charts.

**Study topic:** None needed — both already prepped from prior phases.

---

## Phase 8 — Documentation
**Status:** ⬜ Not Started

- [ ] **Fill in `docs/ARCHITECTURE.md`** — Owner: Himanshu — Document Bronze/Silver/Gold mapping, draw the pipeline diagram (Eraser.io). Goal: anyone understands data flow without reading code.
- [ ] **Fill in `docs/DESIGN.md`** — Owner: Tamanna — Document schema rationale, grain decision consequences, age-parsing approach. Goal: defend every schema decision in writing.

**Definition of Done:** Each person reviews the other's doc and finds no gaps they can't explain.

---

## Phase 9 — Final Validation
**Status:** ⬜ Not Started

- [ ] **Run all success criteria** — Owner: Both — Pipeline under 2 minutes, nulls under 1%, grain correct, India query returns one row.
- [ ] **Cross-explain walkthrough** — Owner: Both — Each person explains the *other's* owned phases out loud, no notes. Goal: confirm both can defend the entire project in an interview.

**Definition of Done:** Both can explain every phase without gaps.

---

### Updating this file
1. Edit `[ ]` → `[x]` for each completed task.
2. Update the phase `**Status:**` line (⬜ Not Started → 🔄 In Progress → ✅ Complete) once any box in that phase is checked.
3. Update the `Progress: X / 10 phases complete` line at the top.
4. Commit: `git add task_list.md && git commit -m "Phase N: mark [task] complete"`