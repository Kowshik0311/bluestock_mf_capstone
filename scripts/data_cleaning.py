"""
Bluestock Fintech — Mutual Fund Analytics Capstone
Day 2: Data Cleaning Script
Author: Kowshik Athreya
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
RAW_DIR   = BASE_DIR / "data" / "raw"
PROC_DIR  = BASE_DIR / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)

# ─── Helper ──────────────────────────────────────────────────────────────────
def section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

# ═══════════════════════════════════════════════════════════════
# 1. CLEAN nav_history.csv
# ═══════════════════════════════════════════════════════════════
section("1. Cleaning nav_history.csv")

nav = pd.read_csv(RAW_DIR / "02_nav_history.csv")
print(f"  Raw shape: {nav.shape}")

# Parse dates
nav["date"] = pd.to_datetime(nav["date"], errors="coerce")

# Sort by fund + date
nav = nav.sort_values(["amfi_code", "date"]).reset_index(drop=True)

# Remove duplicates
before = len(nav)
nav = nav.drop_duplicates(subset=["amfi_code", "date"])
print(f"  Duplicates removed: {before - len(nav)}")

# Forward-fill missing NAV (weekends/holidays)
nav = nav.set_index("date").groupby("amfi_code").apply(
    lambda x: x.reindex(
        pd.date_range(x.index.min(), x.index.max(), freq="B")
    ).ffill()
).reset_index(level=0, drop=True).reset_index()
nav.rename(columns={"index": "date"}, inplace=True)

# Validate NAV > 0
invalid = nav[nav["nav"] <= 0]
if not invalid.empty:
    print(f"  ⚠ Invalid NAV rows (<=0): {len(invalid)}")
    nav = nav[nav["nav"] > 0]
else:
    print("  ✓ All NAV values are positive")

# Drop any remaining nulls
nav = nav.dropna(subset=["nav", "date"])

print(f"  Clean shape: {nav.shape}")
nav.to_csv(PROC_DIR / "clean_nav_history.csv", index=False)
print("  ✅ Saved: clean_nav_history.csv")

# ═══════════════════════════════════════════════════════════════
# 2. CLEAN investor_transactions.csv
# ═══════════════════════════════════════════════════════════════
section("2. Cleaning investor_transactions.csv")

tx = pd.read_csv(RAW_DIR / "08_investor_transactions.csv")
print(f"  Raw shape: {tx.shape}")

# Standardise transaction_type
tx["transaction_type"] = tx["transaction_type"].str.strip().str.title()
print(f"  Transaction types: {tx['transaction_type'].unique()}")

# Parse dates
tx["transaction_date"] = pd.to_datetime(tx["transaction_date"], errors="coerce")

# Remove rows where amount <= 0
before = len(tx)
tx = tx[tx["amount_inr"] > 0]
print(f"  Removed {before - len(tx)} rows with amount <= 0")

# Drop duplicates
before = len(tx)
tx = tx.drop_duplicates()
print(f"  Duplicates removed: {before - len(tx)}")

# Check KYC status
print(f"  KYC status values: {tx['kyc_status'].unique()}")

# Drop nulls in key columns
tx = tx.dropna(subset=["investor_id", "transaction_date", "amfi_code", "amount_inr"])

print(f"  Clean shape: {tx.shape}")
tx.to_csv(PROC_DIR / "clean_investor_transactions.csv", index=False)
print("  ✅ Saved: clean_investor_transactions.csv")

# ═══════════════════════════════════════════════════════════════
# 3. CLEAN scheme_performance.csv
# ═══════════════════════════════════════════════════════════════
section("3. Cleaning scheme_performance.csv")

perf = pd.read_csv(RAW_DIR / "07_scheme_performance.csv")
print(f"  Raw shape: {perf.shape}")

# Validate numeric return columns
return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
               "sharpe_ratio", "alpha", "beta"]
for col in return_cols:
    if col in perf.columns:
        perf[col] = pd.to_numeric(perf[col], errors="coerce")

# Flag negative Sharpe ratios
neg_sharpe = perf[perf["sharpe_ratio"] < 0]
if not neg_sharpe.empty:
    print(f"  ⚠ Funds with negative Sharpe ratio: {len(neg_sharpe)}")
    print(f"    {neg_sharpe['amfi_code'].tolist()}")
else:
    print("  ✓ No negative Sharpe ratios")

# Validate expense ratio range
if "expense_ratio_pct" in perf.columns:
    out_of_range = perf[
        (perf["expense_ratio_pct"] < 0.1) | (perf["expense_ratio_pct"] > 2.5)
    ]
    if not out_of_range.empty:
        print(f"  ⚠ Expense ratio out of range: {len(out_of_range)} rows")
    else:
        print("  ✓ All expense ratios in valid range (0.1% – 2.5%)")

print(f"  Clean shape: {perf.shape}")
perf.to_csv(PROC_DIR / "clean_scheme_performance.csv", index=False)
print("  ✅ Saved: clean_scheme_performance.csv")

# ═══════════════════════════════════════════════════════════════
# 4. CLEAN remaining datasets
# ═══════════════════════════════════════════════════════════════
other_files = {
    "01_fund_master.csv":         "clean_fund_master.csv",
    "03_aum_by_fund_house.csv":   "clean_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv": "clean_monthly_sip_inflows.csv",
    "05_category_inflows.csv":    "clean_category_inflows.csv",
    "06_industry_folio_count.csv":"clean_industry_folio_count.csv",
    "09_portfolio_holdings.csv":  "clean_portfolio_holdings.csv",
    "10_benchmark_indices.csv":   "clean_benchmark_indices.csv",
}

for raw_file, clean_file in other_files.items():
    section(f"Cleaning {raw_file}")
    df = pd.read_csv(RAW_DIR / raw_file)
    print(f"  Raw shape: {df.shape}")

    # Drop full duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    print(f"  Duplicates removed: {before - len(df)}")

    # Report missing values
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if not nulls.empty:
        print(f"  ⚠ Missing values:\n{nulls}")
        df = df.ffill().bfill()
        print(f"  ✓ Missing values filled")
    else:
        print(f"  ✓ No missing values")

    print(f"  Clean shape: {df.shape}")
    df.to_csv(PROC_DIR / clean_file, index=False)
    print(f"  ✅ Saved: {clean_file}")

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════
section("CLEANING COMPLETE")
clean_files = list(PROC_DIR.glob("*.csv"))
print(f"  Total clean files saved: {len(clean_files)}")
for f in sorted(clean_files):
    print(f"    ✅ {f.name}")

print("\n✅ data_cleaning.py completed successfully!")