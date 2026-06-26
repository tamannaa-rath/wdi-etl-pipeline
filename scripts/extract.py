"""
Reads the raw SDMX export in fixed-size chunks (file -> 3.8 GB,8,894,932 rows.
- too large to load in one short on my machine).

Drop columns confirmed constant or structurally irrelevant via the 
cardinality check(see docs/DATA_DICTIONARY.md for the full reasoning).
Does NOT collapse CODE/LABEL pairs, parse AGE codes, or handle nulls-(will done in clean.py)

This script is a GENERATOR. It yields chunks (DataFrames) one at a time.
clean.py will receive these chunks and process them on the fly.
Memory usage stays flat (~500MB) regardless of the source file size.

Usage:
    uv run python scripts/extract.py data/raw/WB_WDI.csv
    uv run python scripts/extract.py data/samples/sample_5000.csv   # for sample testing
"""

import sys
from pathlib import Path 
import pandas as pd

# columns to drop
drop_cols = [
    "STRUCTURE", "STRUCTURE_ID", "ACTION",
    "FREQ", "FREQ_LABEL",
    "OBS_STATUS", "OBS_STATUS_LABEL",
    "COMP_BREAKDOWN_1", "COMP_BREAKDOWN_1_LABEL",
    "COMP_BREAKDOWN_2", "COMP_BREAKDOWN_2_LABEL",
    "COMP_BREAKDOWN_3", "COMP_BREAKDOWN_3_LABEL",
    "AGG_METHOD", "AGG_METHOD_LABEL",
    "UNIT_TYPE", "UNIT_TYPE_LABEL",
    "DECIMALS", "DECIMALS_LABEL",
    "DATABASE_ID", "DATABASE_ID_LABEL",
    "TIME_FORMAT", "TIME_FORMAT_LABEL",
    "UNIT_MULT", "UNIT_MULT_LABEL",
    "OBS_CONF", "OBS_CONF_LABEL",
]

# no. of rows to pull
chunk_size= 100_000

def extract_chunks(input_path:str):
    """
    A generator that yields cleaned chunks of the CSV.

    Yields:
        pd.DataFrame: A chunk with constant/plumbing columns dropped.
    """
    file_path= Path(input_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Cannot find {input_path}")
    
    total_rows_read= 0

    # CSV reader
    reader = pd.read_csv(file_path,chunksize=chunk_size, low_memory=False)

    for i, chunk in enumerate(reader):
        total_rows_read += len(chunk)

        #Drop columns that exist in this chunk
        cols_to_drop = [c for c in drop_cols if c in chunk.columns]
        if cols_to_drop:
            chunk= chunk.drop(columns=cols_to_drop)
        
        print(f" [Extract] Chunk {i+1}: {len(chunk)} rows read. Total so far: {total_rows_read}")

        #YIELD: Send this chunk to the caller (clean.py) and PAUSE execution
        #memory is freed once clean.py finishes with this chunk.
        yield chunk
    
    print(f"\n[Extract] Extraction complete. Total rows streamed: {total_rows_read}")

def verify_row_integrity(input_path: str, total_extracted_rows: int) -> bool:
    """
    cross-check: count actual lines in the source file (minus header) and compare
    against rows extracted. Catches silent row loss.

    Note: This opens the file seperately. Only run this during initial testing,
    not on every pipeline run (it adds an extra 30 sec to scan 3.8GB).
    """
    with open(input_path, "r", encoding="utf-8",errors="replace") as f:
        line_count = sum(1 for _ in f) - 1 # minus header row
    
    matches = (line_count == total_extracted_rows)
    print(f"\n[Integrity Check] File has {line_count} rows, Extracted {total_extracted_rows} -> {'✅ MATCH' if matches else '❌ MISMATCH'}")
    return matches

if __name__ == "__main__":
    # main block to run furst
    # it test the generator by counting all rows and verifying integrity.

    if len(sys.argv) != 2:
        print("Usage: uv run python scripts/extract.py <path_to_csv>")
        sys.exit(1)
    
    csv_path = sys.argv[1]

    # text generator
    total = 0
    for chunk in extract_chunks(csv_path):
        total += len(chunk)
    
    # verifying integrity 
    verify_row_integrity(csv_path,total)