# Data Dictionary

This document records what every column in the raw `WB_WDI.csv` export means, and the decision made for each one: **kept as a dimension**, **kept on the fact table**, or **dropped**.

Decisions were made using a cardinality check — sampling 50,000 rows from two non-overlapping sections of the file (rows 0–50k and rows 4,000,000–4,050,000) and counting distinct values per column. A column with real, repeating variation becomes a dimension. A column that's constant across the dataset carries no information and is dropped.

## Source

- **Dataset:** World Bank World Development Indicators (WDI)
- **Export format:** SDMX (Statistical Data and Metadata eXchange)
- **Raw file:** `WB_WDI.csv` — 8,894,932 rows, 41 columns, 3.6GB

## Columns Kept as Dimensions

| Raw Column | Sample Values | Distinct Count | Becomes | Notes |
|---|---|---|---|---|
| `REF_AREA` / `REF_AREA_LABEL` | `IND` / `India` | ~217 countries | `dim_country` | Code + label pair collapsed into one table |
| `INDICATOR` / `INDICATOR_LABEL` | `NY.GDP.PCAP.KD` / `GDP per capita` | ~1,400 indicators | `dim_indicator` | Also carries `UNIT_MEASURE` |
| `TIME_PERIOD` | `2020` | 66 years (1960–2025) | `dim_date` | Simple year dimension |
| `SEX` / `SEX_LABEL` | `_T`, `F`, `M` | 3 | `dim_sex` | `_T` = Total (SDMX convention for "not broken down") |
| `AGE` / `AGE_LABEL` | `_T`, `Y15T24`, `Y10T14`, ... | 22 | `dim_age` | `Y##T##` = age band, e.g. `Y15T24` = ages 15–24. Needs a parser. |
| `URBANISATION` / `URBANISATION_LABEL` | `_T`, `RUR`, `URB` | 3 | `dim_urbanisation` | Total / Rural / Urban |

## Columns Kept on the Fact Table

| Raw Column | Becomes | Notes |
|---|---|---|
| `OBS_VALUE` | `obs_value` | The actual measurement — this is the fact |

## Columns Dropped (Confirmed Constant)

Verified constant across two independent 50k-row samples taken ~4 million rows apart:

| Raw Column | Value (always) | Meaning | Why Dropped |
|---|---|---|---|
| `FREQ` | `A` | Annual | Dataset-level metadata, not per-observation — WDI is annual-only |
| `OBS_STATUS` | `A` | "Actual/Normal" (not estimated/provisional) | No variation found in 100k sampled rows; re-verify if full-load row counts look suspicious |
| `COMP_BREAKDOWN_1` | `_Z` | "Not applicable" | Unused SDMX breakdown slot in this extract |
| `COMP_BREAKDOWN_2` | `_Z` | "Not applicable" | Unused SDMX breakdown slot in this extract |
| `COMP_BREAKDOWN_3` | `_Z` | "Not applicable" | Unused SDMX breakdown slot in this extract |

## Columns Dropped (SDMX Structural Plumbing)

These describe the *shape* of the SDMX export itself, not the data — never vary in a way relevant to analysis:

`STRUCTURE`, `STRUCTURE_ID`, `ACTION`, `DATABASE_ID`, `DATABASE_ID_LABEL`, `TIME_FORMAT`, `TIME_FORMAT_LABEL`, `DECIMALS`, `DECIMALS_LABEL`, `UNIT_MULT`, `UNIT_MULT_LABEL`, `AGG_METHOD`, `AGG_METHOD_LABEL`, `UNIT_TYPE`, `UNIT_TYPE_LABEL`, `OBS_CONF`, `OBS_CONF_LABEL`, `FREQ_LABEL`, `OBS_STATUS_LABEL`, `COMP_BREAKDOWN_1_LABEL`, `COMP_BREAKDOWN_2_LABEL`, `COMP_BREAKDOWN_3_LABEL`

## SDMX Code Reference

Common codes seen in this dataset, decoded:

| Code | Meaning |
|---|---|
| `_T` | Total (no breakdown applied) |
| `_Z` | Not applicable |
| `M` | Male |
| `F` | Female |
| `RUR` | Rural |
| `URB` | Urban |
| `A` (in FREQ) | Annual |
| `A` (in OBS_STATUS) | Actual / Normal value |
| `Y##T##` (in AGE) | Age band from ## to ## years, e.g. `Y15T24` = 15 to 24 years |

## Open Question

`AGE` has 22 distinct codes that need full decoding (not all are simple `Y##T##` ranges — some may be `Y_GE65` style "65 and over" codes). Full lookup table to be built when `dim_age` is implemented — owner TBD.