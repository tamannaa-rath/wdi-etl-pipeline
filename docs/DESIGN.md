# Design Rationale

> Status: stub. Fill in as the build progresses — this should read like a defense of every schema decision, not just a restatement of the schema.

## TODO

- [ ] Star schema diagram (link from `docs/diagrams/star-schema.png`)
- [ ] Why 5 dimensions, not fewer — restate the cardinality check reasoning from `DATA_DICTIONARY.md` in design terms
- [ ] Fact table grain: one row = one (country, indicator, year, sex, age, urbanisation) combination. Document the consequence: a "simple" lookup like *India's GDP per capita in 2020* returns multiple rows unless filtered to `sex = '_T' AND age = '_T' AND urbanisation = '_T'`
- [ ] `dim_age` parsing strategy — how `Y15T24`-style codes get decoded into readable labels
- [ ] Indexing decisions on the fact table (which FKs get indexed, why)
- [ ] Any normalization tradeoffs made for query performance