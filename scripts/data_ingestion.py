"""
Bluestock Fintech — Mutual Fund Analytics Platform
=================================================
Script  : data_ingestion.py
Purpose : Load all 10 raw CSV datasets and fetch live NAV data from mfapi.in
Author  : Kowshik Athreya
Date    : June 2026
"""

import pandas as pd
from pathlib import Path

# ─── Path Configuration ───────────────────────────────────────────────────────
# Using pathlib for cross-platform compatibility (avoids hardcoded paths)
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR  = BASE_DIR / "data" / "raw"

# ─── Dataset Registry ────────────────────────────────────────────────────────
# All 10 provided CSV datasets from Bluestock Fintech / AMFI India
DATASETS = [
    "01_fund_master.csv",          # Master list of 40 fund schemes
    "02_nav_history.csv",          # Daily NAV history 2022-2026
    "03_aum_by_fund_house.csv",    # Quarterly AUM by fund house
    "04_monthly_sip_inflows.csv",  # Monthly SIP inflow data
    "05_category_inflows.csv",     # Net inflows by fund category
    "06_industry_folio_count.csv", # Total MF folios over time
    "07_scheme_performance.csv",   # Performance metrics per scheme
    "08_investor_transactions.csv",# Investor SIP/Lumpsum/Redemption data
    "09_portfolio_holdings.csv",   # Top equity holdings per fund
    "10_benchmark_indices.csv",    # Nifty 50, Nifty 100, BSE SmallCap
]


def load_dataset(filepath: Path) -> pd.DataFrame:
    """
    Load a single CSV file into a Pandas DataFrame.

    Args:
        filepath: Full path to the CSV file

    Returns:
        DataFrame with the loaded data, or None if file not found
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"  ❌ File not found: {filepath}")
        return None


def inspect_dataset(df: pd.DataFrame, filename: str) -> None:
    """
    Print key metadata about a DataFrame for quality checking.

    Args:
        df      : The loaded DataFrame
        filename: Name of the source file (for display)
    """
    print(f"\n{'='*60}")
    print(f"  File    : {filename}")
    print(f"  Shape   : {df.shape}")
    print(f"  Columns : {list(df.columns)}")
    print(f"  Dtypes  :\n{df.dtypes}")
    print(f"\n  Head (3 rows):\n{df.head(3)}")

    # Check for missing values
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if not nulls.empty:
        print(f"\n  ⚠ Missing values detected:\n{nulls}")
    else:
        print(f"\n  ✓ No missing values found")


def validate_amfi_codes(fund_master: pd.DataFrame,
                         nav_history: pd.DataFrame) -> None:
    """
    Validate that every AMFI code in fund_master exists in nav_history.
    This ensures data integrity before loading into the database.

    Args:
        fund_master : DataFrame containing the fund master list
        nav_history : DataFrame containing NAV history records
    """
    print("\n--- AMFI Code Validation ---")

    master_codes = set(fund_master["amfi_code"].astype(str))
    nav_codes    = set(nav_history["amfi_code"].astype(str)) \
                   if "amfi_code" in nav_history.columns else set()

    missing = master_codes - nav_codes
    extra   = nav_codes - master_codes

    if not missing:
        print("  ✓ All fund_master AMFI codes found in nav_history")
    else:
        print(f"  ⚠ Missing in nav_history: {missing}")

    print(f"\n  Data Quality Summary:")
    print(f"    fund_master codes : {len(master_codes)}")
    print(f"    nav_history codes : {len(nav_codes)}")
    print(f"    Missing codes     : {len(missing)}")
    print(f"    Extra codes       : {len(extra)}")


# ─── Main Execution ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Starting data ingestion...")
    dataframes = {}

    # Load and inspect all 10 datasets
    for filename in DATASETS:
        df = load_dataset(RAW_DIR / filename)
        if df is not None:
            inspect_dataset(df, filename)
            dataframes[filename] = df

    print(f"\n{'='*60}")
    print(f"✅ Loaded {len(dataframes)} / {len(DATASETS)} datasets")

    # Explore fund master
    print("\n--- Fund Master Exploration ---")
    fm = dataframes.get("01_fund_master.csv")
    if fm is not None:
        print(f"  Fund Houses     : {fm['fund_house'].nunique()}")
        print(f"  Categories      : {fm['category'].unique()}")
        print(f"  Sub-Categories  : {fm['sub_category'].unique()}")
        print(f"  Risk Grades     : {fm['risk_category'].unique()}")

    # Validate AMFI codes
    fm  = dataframes.get("01_fund_master.csv")
    nav = dataframes.get("02_nav_history.csv")
    if fm is not None and nav is not None:
        validate_amfi_codes(fm, nav)

    print("\n✅ data_ingestion.py completed successfully!")