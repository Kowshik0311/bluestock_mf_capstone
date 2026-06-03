"""
Bluestock Fintech — Mutual Fund Analytics Capstone
Day 2: SQLite Database Creation + Data Load Script
Author: Kowshik Athreya
"""

import pandas as pd
import sqlite3
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
PROC_DIR = BASE_DIR / "data" / "processed"
DB_DIR   = BASE_DIR / "data" / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH  = DB_DIR / "bluestock_mf.db"

# ─── Connect to SQLite ───────────────────────────────────────────────────────
conn = sqlite3.connect(DB_PATH)
cur  = conn.cursor()
print(f"✅ Connected to database: {DB_PATH}")

# ─── Create Tables ───────────────────────────────────────────────────────────
print("\n--- Creating Tables ---")

cur.executescript("""
-- Dimension: Fund Master
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code       TEXT PRIMARY KEY,
    fund_house      TEXT,
    scheme_name     TEXT,
    category        TEXT,
    sub_category    TEXT,
    plan            TEXT,
    benchmark       TEXT,
    expense_ratio_pct REAL,
    risk_category   TEXT,
    fund_manager    TEXT
);

-- Fact: NAV History
CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code       TEXT,
    date            TEXT,
    nav             REAL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Investor Transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    tx_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id         TEXT,
    transaction_date    TEXT,
    amfi_code           TEXT,
    transaction_type    TEXT,
    amount_inr          REAL,
    state               TEXT,
    city                TEXT,
    city_tier           TEXT,
    age_group           TEXT,
    gender              TEXT,
    payment_mode        TEXT,
    kyc_status          TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Scheme Performance
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code           TEXT PRIMARY KEY,
    return_1yr_pct      REAL,
    return_3yr_pct      REAL,
    return_5yr_pct      REAL,
    sharpe_ratio        REAL,
    sortino_ratio       REAL,
    alpha               REAL,
    beta                REAL,
    max_drawdown_pct    REAL,
    std_dev_ann_pct     REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: AUM by Fund House
CREATE TABLE IF NOT EXISTS fact_aum (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house  TEXT,
    date        TEXT,
    aum_crore   REAL
);

-- Fact: Monthly SIP Inflows
CREATE TABLE IF NOT EXISTS fact_sip_inflows (
    month                   TEXT PRIMARY KEY,
    sip_inflow_crore        REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh   REAL,
    sip_aum_lakh_crore      REAL
);

-- Fact: Portfolio Holdings
CREATE TABLE IF NOT EXISTS fact_portfolio (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code   TEXT,
    stock_symbol TEXT,
    weight_pct  REAL,
    sector      TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- Fact: Benchmark Indices
CREATE TABLE IF NOT EXISTS fact_benchmark (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT,
    index_name  TEXT,
    close_value REAL
);
""")

conn.commit()
print("  ✅ All tables created successfully")

# ─── Load Data ───────────────────────────────────────────────────────────────
print("\n--- Loading Data into Tables ---")

def load_table(csv_file, table_name, if_exists="replace"):
    filepath = PROC_DIR / csv_file
    if not filepath.exists():
        print(f"  ⚠ File not found: {csv_file}")
        return
    df = pd.read_csv(filepath)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    print(f"  ✅ Loaded {len(df):,} rows into '{table_name}'")

load_table("clean_fund_master.csv",          "dim_fund")
load_table("clean_nav_history.csv",          "fact_nav")
load_table("clean_investor_transactions.csv","fact_transactions")
load_table("clean_scheme_performance.csv",   "fact_performance")
load_table("clean_aum_by_fund_house.csv",    "fact_aum")
load_table("clean_monthly_sip_inflows.csv",  "fact_sip_inflows")
load_table("clean_portfolio_holdings.csv",   "fact_portfolio")
load_table("clean_benchmark_indices.csv",    "fact_benchmark")

# ─── Run 10 SQL Queries ──────────────────────────────────────────────────────
print("\n--- Running 10 Analytical SQL Queries ---")

queries = {
    "1. Top 5 funds by expense ratio": """
        SELECT scheme_name, fund_house, expense_ratio_pct
        FROM dim_fund
        ORDER BY expense_ratio_pct DESC
        LIMIT 5
    """,
    "2. Funds with expense ratio < 1%": """
        SELECT scheme_name, fund_house, expense_ratio_pct
        FROM dim_fund
        WHERE expense_ratio_pct < 1.0
        ORDER BY expense_ratio_pct ASC
    """,
    "3. Top 5 funds by 3yr return": """
        SELECT d.scheme_name, d.fund_house, p.return_3yr_pct
        FROM fact_performance p
        JOIN dim_fund d ON p.amfi_code = d.amfi_code
        ORDER BY p.return_3yr_pct DESC
        LIMIT 5
    """,
    "4. Top 5 funds by Sharpe ratio": """
        SELECT d.scheme_name, p.sharpe_ratio
        FROM fact_performance p
        JOIN dim_fund d ON p.amfi_code = d.amfi_code
        ORDER BY p.sharpe_ratio DESC
        LIMIT 5
    """,
    "5. Transaction count by type": """
        SELECT transaction_type, COUNT(*) as count,
               ROUND(SUM(amount_inr),2) as total_amount
        FROM fact_transactions
        GROUP BY transaction_type
    """,
    "6. Top 5 states by SIP amount": """
        SELECT state, ROUND(SUM(amount_inr),2) as total_sip
        FROM fact_transactions
        WHERE transaction_type = 'Sip'
        GROUP BY state
        ORDER BY total_sip DESC
        LIMIT 5
    """,
    "7. Transactions by age group": """
        SELECT age_group, COUNT(*) as count,
               ROUND(AVG(amount_inr),2) as avg_amount
        FROM fact_transactions
        GROUP BY age_group
        ORDER BY avg_amount DESC
    """,
    "8. Fund count by category": """
        SELECT category, sub_category, COUNT(*) as num_funds
        FROM dim_fund
        GROUP BY category, sub_category
        ORDER BY num_funds DESC
    """,
    "9. Latest NAV per fund (top 10)": """
        SELECT n.date, n.nav
        FROM fact_nav n
        ORDER BY n.nav DESC
        LIMIT 10
    """,
    "10. T30 vs B30 transaction split": """
        SELECT city_tier,
               COUNT(*) as transactions,
               ROUND(SUM(amount_inr)/1e7, 2) as total_crore
        FROM fact_transactions
        GROUP BY city_tier
    """,
}

for title, sql in queries.items():
    print(f"\n  {title}")
    result = pd.read_sql_query(sql, conn)
    print(result.to_string(index=False))

conn.close()
print("\n" + "=" * 60)
print("✅ create_database.py completed successfully!")
print(f"   Database saved at: data/db/bluestock_mf.db")