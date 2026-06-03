"""
Bluestock Fintech — Mutual Fund Analytics Capstone
Day 1: Data Ingestion Script
Author: Kowshik Athreya
"""

import pandas as pd
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR  = BASE_DIR / "data" / "raw"

# ─── Dataset filenames ───────────────────────────────────────────────────────
DATASETS = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

# ─── Load & inspect each dataset ─────────────────────────────────────────────
dataframes = {}

for filename in DATASETS:
    filepath = RAW_DIR / filename
    print("=" * 60)
    print(f"Loading: {filename}")

    try:
        df = pd.read_csv(filepath)
        dataframes[filename] = df

        print(f"  Shape     : {df.shape}")
        print(f"  Columns   : {list(df.columns)}")
        print(f"  Dtypes    :\n{df.dtypes}")
        print(f"\n  Head (3 rows):\n{df.head(3)}")

        # Check for missing values
        nulls = df.isnull().sum()
        nulls = nulls[nulls > 0]
        if not nulls.empty:
            print(f"\n  ⚠ Missing values:\n{nulls}")
        else:
            print(f"\n  ✓ No missing values found")

    except FileNotFoundError:
        print(f"  ❌ File not found: {filepath}")

print("\n" + "=" * 60)
print(f"✅ Done! Loaded {len(dataframes)} / {len(DATASETS)} datasets successfully.")

# ─── Fund Master: unique values exploration ──────────────────────────────────
print("\n--- Fund Master Exploration ---")
fm = dataframes.get("01_fund_master.csv")
if fm is not None:
    print(f"Unique Fund Houses  : {fm['fund_house'].nunique()}")
    print(fm['fund_house'].unique())
    print(f"\nUnique Categories   : {fm['category'].unique()}")
    print(f"Unique Sub-Categories: {fm['sub_category'].unique()}")
    print(f"Risk Grades         : {fm['risk_category'].unique()}")

# ─── AMFI Code Validation ────────────────────────────────────────────────────
print("\n--- AMFI Code Validation ---")
fm       = dataframes.get("01_fund_master.csv")
nav_hist = dataframes.get("02_nav_history.csv")

if fm is not None and nav_hist is not None:
    master_codes = set(fm['amfi_code'].astype(str))
    nav_codes    = set(nav_hist['amfi_code'].astype(str))

    missing_in_nav = master_codes - nav_codes
    extra_in_nav   = nav_codes - master_codes

    if not missing_in_nav:
        print("  ✓ All fund_master AMFI codes found in nav_history")
    else:
        print(f"  ⚠ Codes in fund_master but missing in nav_history: {missing_in_nav}")

    if extra_in_nav:
        print(f"  ⚠ Codes in nav_history but not in fund_master: {extra_in_nav}")

    print("\n  Data Quality Summary:")
    print(f"    fund_master codes : {len(master_codes)}")
    print(f"    nav_history codes : {len(nav_codes)}")
    print(f"    Missing codes     : {len(missing_in_nav)}")
    print(f"    Extra codes       : {len(extra_in_nav)}")

print("\n✅ data_ingestion.py completed successfully!")