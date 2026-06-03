"""
Bluestock Fintech — Mutual Fund Analytics Capstone
Day 1: Live NAV Fetch Script (mfapi.in)
Author: Kowshik Athreya
"""

import requests
import pandas as pd
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR  = BASE_DIR / "data" / "raw"

# ─── Fund schemes to fetch ───────────────────────────────────────────────────
SCHEMES = {
    "HDFC_Top_100":      125497,
    "SBI_Bluechip":      119551,
    "ICICI_Bluechip":    120503,
    "Nippon_Large_Cap":  118632,
    "Axis_Bluechip":     119092,
    "Kotak_Bluechip":    120841,
}

BASE_URL = "https://api.mfapi.in/mf/{}"

# ─── Fetch & save each scheme ────────────────────────────────────────────────
for scheme_name, code in SCHEMES.items():
    print("=" * 60)
    print(f"Fetching: {scheme_name} (Code: {code})")

    try:
        url      = BASE_URL.format(code)
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract scheme metadata
        meta = data.get("meta", {})
        print(f"  Fund House : {meta.get('fund_house', 'N/A')}")
        print(f"  Scheme Name: {meta.get('scheme_name', 'N/A')}")
        print(f"  Scheme Type: {meta.get('scheme_type', 'N/A')}")

        # Extract NAV history
        nav_data = data.get("data", [])
        df = pd.DataFrame(nav_data)
        df.columns = ["date", "nav"]
        df["nav"]  = pd.to_numeric(df["nav"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        df         = df.sort_values("date").reset_index(drop=True)
        df["amfi_code"]    = code
        df["scheme_name"]  = meta.get("scheme_name", scheme_name)
        df["fund_house"]   = meta.get("fund_house", "N/A")

        print(f"  Records    : {len(df)}")
        print(f"  Date Range : {df['date'].min().date()} to {df['date'].max().date()}")
        print(f"  Latest NAV : Rs. {df['nav'].iloc[-1]:.4f}")
        print(f"\n  Sample:\n{df.tail(3)}")

        # Save to raw folder
        filename = RAW_DIR / f"live_nav_{scheme_name}.csv"
        df.to_csv(filename, index=False)
        print(f"\n  ✅ Saved to: {filename.name}")

    except requests.exceptions.ConnectionError:
        print(f"  ❌ Connection error — check your internet connection")
    except requests.exceptions.Timeout:
        print(f"  ❌ Request timed out for {scheme_name}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ live_nav_fetch.py completed successfully!")
print(f"   Check data/raw/ for live_nav_*.csv files")