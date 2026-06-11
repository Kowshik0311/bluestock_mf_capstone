"""
Bluestock Fintech — Mutual Fund Analytics Platform
=================================================
Script  : data_cleaning.py
Purpose : Clean and validate all 10 raw datasets for analysis
Author  : Kowshik Athreya
Date    : June 2026

Cleaning Operations:
    - Parse date columns to datetime format
    - Remove duplicate rows
    - Forward-fill missing NAV values (weekends/holidays)
    - Validate numeric ranges (NAV > 0, expense ratio 0.1-2.5%)
    - Standardise categorical values (transaction types)
    - Save cleaned files to data/processed/
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ─── Path Configuration ───────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
RAW_DIR   = BASE_DIR / "data" / "raw"
PROC_DIR  = BASE_DIR / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)


def section(title: str) -> None:
    """Print a formatted section header for console output."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def clean_nav_history(filepath: Path) -> pd.DataFrame:
    """
    Clean the NAV history dataset.

    Operations:
        - Parse date column to datetime
        - Sort by date
        - Remove duplicates
        - Forward-fill missing NAV for weekends/holidays
        - Remove rows where NAV <= 0

    Args:
        filepath: Path to raw nav_history CSV

    Returns:
        Cleaned DataFrame
    """
    section("Cleaning nav_history.csv")
    nav = pd.read_csv(filepath)
    print(f"  Raw shape: {nav.shape}")

    # Parse dates
    nav["date"] = pd.to_datetime(nav["date"], errors="coerce")

    # Sort by date
    nav = nav.sort_values("date").reset_index(drop=True)

    # Remove duplicates
    before = len(nav)
    nav = nav.drop_duplicates()
    print(f"  Duplicates removed: {before - len(nav)}")

    # Forward-fill missing NAV
    nav = nav.set_index("date")
    nav = nav[~nav.index.duplicated(keep="first")]
    nav = nav.reindex(pd.date_range(nav.index.min(),
                                 nav.index.max(), freq="B")).ffill()
    nav = nav.reset_index().rename(columns={"index": "date"})

    # Validate NAV > 0
    invalid = nav[nav["nav"] <= 0]
    if not invalid.empty:
        print(f"  ⚠ Invalid NAV rows removed: {len(invalid)}")
        nav = nav[nav["nav"] > 0]
    else:
        print("  ✓ All NAV values are positive")

    # Drop nulls
    nav = nav.dropna(subset=["nav", "date"])

    print(f"  Clean shape: {nav.shape}")
    return nav


def clean_transactions(filepath: Path) -> pd.DataFrame:
    """
    Clean the investor transactions dataset.

    Operations:
        - Standardise transaction_type to Title Case
        - Parse transaction_date to datetime
        - Remove rows where amount_inr <= 0
        - Remove duplicate rows
        - Drop rows with null key columns

    Args:
        filepath: Path to raw investor_transactions CSV

    Returns:
        Cleaned DataFrame
    """
    section("Cleaning investor_transactions.csv")
    tx = pd.read_csv(filepath)
    print(f"  Raw shape: {tx.shape}")

    # Standardise transaction type
    tx["transaction_type"] = tx["transaction_type"].str.strip().str.title()
    print(f"  Transaction types: {tx['transaction_type'].unique()}")

    # Parse dates
    tx["transaction_date"] = pd.to_datetime(tx["transaction_date"],
                                             errors="coerce")

    # Remove invalid amounts
    before = len(tx)
    tx = tx[tx["amount_inr"] > 0]
    print(f"  Removed {before - len(tx)} rows with amount <= 0")

    # Remove duplicates
    before = len(tx)
    tx = tx.drop_duplicates()
    print(f"  Duplicates removed: {before - len(tx)}")

    # Drop nulls in key columns
    tx = tx.dropna(subset=["investor_id", "transaction_date",
                            "amfi_code", "amount_inr"])

    print(f"  Clean shape: {tx.shape}")
    return tx


def clean_performance(filepath: Path) -> pd.DataFrame:
    """
    Clean the scheme performance dataset.

    Operations:
        - Validate return columns are numeric
        - Flag negative Sharpe ratios
        - Check expense ratio range (0.1% - 2.5%)

    Args:
        filepath: Path to raw scheme_performance CSV

    Returns:
        Cleaned DataFrame
    """
    section("Cleaning scheme_performance.csv")
    perf = pd.read_csv(filepath)
    print(f"  Raw shape: {perf.shape}")

    # Validate numeric columns
    return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
                   "sharpe_ratio", "alpha", "beta"]
    for col in return_cols:
        if col in perf.columns:
            perf[col] = pd.to_numeric(perf[col], errors="coerce")

    # Flag negative Sharpe ratios
    if "sharpe_ratio" in perf.columns:
        neg = perf[perf["sharpe_ratio"] < 0]
        if not neg.empty:
            print(f"  ⚠ Funds with negative Sharpe: {len(neg)}")
        else:
            print("  ✓ No negative Sharpe ratios")

    # Check expense ratio range
    if "expense_ratio_pct" in perf.columns:
        out = perf[(perf["expense_ratio_pct"] < 0.1) |
                   (perf["expense_ratio_pct"] > 2.5)]
        if not out.empty:
            print(f"  ⚠ Expense ratio out of range: {len(out)}")
        else:
            print("  ✓ All expense ratios in valid range")

    print(f"  Clean shape: {perf.shape}")
    return perf


def clean_generic(filepath: Path, name: str) -> pd.DataFrame:
    """
    Generic cleaning function for remaining datasets.

    Operations:
        - Remove duplicate rows
        - Forward-fill and back-fill missing values

    Args:
        filepath: Path to raw CSV
        name    : Display name for console output

    Returns:
        Cleaned DataFrame
    """
    section(f"Cleaning {name}")
    df = pd.read_csv(filepath)
    print(f"  Raw shape: {df.shape}")

    before = len(df)
    df = df.drop_duplicates()
    print(f"  Duplicates removed: {before - len(df)}")

    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if not nulls.empty:
        print(f"  ⚠ Missing values:\n{nulls}")
        df = df.ffill().bfill()
        print("  ✓ Missing values filled")
    else:
        print("  ✓ No missing values")

    print(f"  Clean shape: {df.shape}")
    return df


# ─── Main Execution ───────────────────────────────────────────────────────────
if __name__ == "__main__":

    # Clean key datasets with dedicated functions
    nav  = clean_nav_history(RAW_DIR / "02_nav_history.csv")
    nav.to_csv(PROC_DIR / "clean_nav_history.csv", index=False)
    print("  ✅ Saved: clean_nav_history.csv")

    tx   = clean_transactions(RAW_DIR / "08_investor_transactions.csv")
    tx.to_csv(PROC_DIR / "clean_investor_transactions.csv", index=False)
    print("  ✅ Saved: clean_investor_transactions.csv")

    perf = clean_performance(RAW_DIR / "07_scheme_performance.csv")
    perf.to_csv(PROC_DIR / "clean_scheme_performance.csv", index=False)
    print("  ✅ Saved: clean_scheme_performance.csv")

    # Clean remaining datasets generically
    others = {
        "01_fund_master.csv":          "clean_fund_master.csv",
        "03_aum_by_fund_house.csv":    "clean_aum_by_fund_house.csv",
        "04_monthly_sip_inflows.csv":  "clean_monthly_sip_inflows.csv",
        "05_category_inflows.csv":     "clean_category_inflows.csv",
        "06_industry_folio_count.csv": "clean_industry_folio_count.csv",
        "09_portfolio_holdings.csv":   "clean_portfolio_holdings.csv",
        "10_benchmark_indices.csv":    "clean_benchmark_indices.csv",
    }

    for raw_file, clean_file in others.items():
        df = clean_generic(RAW_DIR / raw_file, raw_file)
        df.to_csv(PROC_DIR / clean_file, index=False)
        print(f"  ✅ Saved: {clean_file}")

    # Final summary
    section("CLEANING COMPLETE")
    clean_files = list(PROC_DIR.glob("clean_*.csv"))
    print(f"  Total clean files: {len(clean_files)}")
    for f in sorted(clean_files):
        print(f"    ✅ {f.name}")

    print("\n✅ data_cleaning.py completed successfully!")