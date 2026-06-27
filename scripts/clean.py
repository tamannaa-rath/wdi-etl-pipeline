DROP_COLUMNS  = [
    "FREQ",
    "OBS_STATUS",
    "COMP_BREAKDOWN_1",
    "COMP_BREAKDOWN_2",
    "COMP_BREAKDOWN_3",
    "SDMX_JSON_SOURCE",
    # other plumbing columns
]

def drop_unused_columns(df):
    """
    Remove unused columns that are not needed.
    """

    return df.drop(columns=DROP_COLUMNS, errors="ignore")



LOOKUP_PAIRS = [
    ("REF_AREA", "REF_AREA_LABEL"),
    ("INDICATOR", "INDICATOR_LABEL"),
    ("SEX", "SEX_LABEL"),
    ("AGE", "AGE_LABEL"),
    ("URBANISATION", "URBANISATION_LABEL"),
    ("UNIT_MEASURE", "UNIT_MEASURE_LABEL"),
]

def validate_lookup_pairs(df):
    """
    Validate that every code/label pair is complete.
    Prints warnings if either column is missing ie mismatched rows.
    """

    for code_col, label_col in LOOKUP_PAIRS:

        # Skip if either column is missing
        if code_col not in df.columns or label_col not in df.columns:
            continue

        invalid_rows = df[
            df[code_col].isna() != df[label_col].isna()
        ]

        if not invalid_rows.empty:
            print(
                f"\n[Warning] {code_col} ↔ {label_col}: "
                f"{len(invalid_rows)} mismatched rows."
            )

            print(
                invalid_rows[[code_col, label_col]]
                .to_string(index=False)
            )

    return df


AGE_MAPPING = {
    "_T": "All age ranges or no breakdown by age",
    "Y0T4": "under 5 years old",
    "Y0T14": "under 15 years old",
    "Y5T9": "5 to 9 years old",
    "Y10T14": "10 to 14 years old",
    "Y15T19": "15 to 19 years old",
    "Y15T24": "15 to 24 years old",
    "Y15T64": "15 to 64 years old",
    "Y20T24": "20 to 24 years old",
    "Y25T34": "25 to 34 years old",
    "Y35T44": "35 to 44 years old",
    "Y45T54": "45 to 54 years old",
    "Y55T64": "55 to 64 years old",
    "Y65T74": "65 to 74 years old",
    "Y75T84": "75 to 84 years old",
    "Y_GE15": "15 years old and over",
    "Y_GE18": "18 years old and over",
    "Y_GE65": "65 years old and over",
    "Y_GE80": "80 years old and over",
    "Y_LT15": "under 15 years old",
    "Y_LT18": "under 18 years old",
}

def parse_age_code(age_code: str) -> str:
    """
    Decode an AGE code into a human-readable label.
    """
    age_code = age_code.strip()

    if age_code not in AGE_MAPPING:
        raise ValueError(f"Unknown AGE code: {age_code}")

    return AGE_MAPPING[age_code]

def parse_age_column(df):
    """
    Decode AGE codes.

    If AGE_LABEL exists:
        Validate it against the parser.

    Otherwise:
        Create AGE_LABEL.
    """
    if df["AGE"].isna().any():
        raise ValueError("AGE contains missing values.")

    expected_labels = df["AGE"].apply(parse_age_code)

    if "AGE_LABEL" in df.columns:

        mismatches = (expected_labels.str.strip() != df["AGE_LABEL"].str.strip())

        if mismatches.any():

            mismatch_rows = df.loc[
                mismatches,
                ["AGE", "AGE_LABEL"]
            ].copy()

            mismatch_rows["EXPECTED_LABEL"] = expected_labels[mismatches]

            raise ValueError(
                f"Found {len(mismatch_rows)} AGE label mismatches:\n\n"
                f"{mismatch_rows.to_string(index=True)}"
            )

    else:

        df["AGE_LABEL"] = expected_labels

    return df


def handle_null_obs_values(df):
    """
    Remove rows where OBS_VALUE is null.
    """

    before = len(df)

    df = df.dropna(subset=["OBS_VALUE"])

    removed = before - len(df)

    if removed:
        print(f"[Clean] Removed {removed} rows with null OBS_VALUE.")

    return df

def clean_chunk(df):
    
    df = drop_unused_columns(df)

    df = validate_lookup_pairs(df)

    df = parse_age_column(df)

    df = handle_null_obs_values(df)

    return df