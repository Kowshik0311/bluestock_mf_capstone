# Data Dictionary — Bluestock MF Analytics Platform
## Author: Kowshik Athreya | June 2026

---

## 01_fund_master.csv
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT | Unique AMFI scheme code (e.g. 125497) |
| fund_house | TEXT | AMC name (e.g. SBI Mutual Fund) |
| scheme_name | TEXT | Full official AMFI scheme name |
| category | TEXT | Equity / Debt / Hybrid |
| sub_category | TEXT | Large Cap / Mid Cap / Small Cap / Liquid etc. |
| plan | TEXT | Regular or Direct |
| launch_date | DATE | Fund launch date |
| benchmark | TEXT | Official benchmark index |
| expense_ratio_pct | REAL | Annual expense ratio % (0.1 to 2.5) |
| exit_load_pct | REAL | Exit load % |
| fund_manager | TEXT | Primary fund manager name |
| risk_category | TEXT | Low / Moderate / Moderately High / High / Very High |

---

## 02_nav_history.csv
| Column | Type | Description |
|---|---|---|
| date | DATE | NAV date (business days only) |
| nav | REAL | NAV in Rs. (e.g. 892.45) |

---

## 03_aum_by_fund_house.csv
| Column | Type | Description |
|---|---|---|
| fund_house | TEXT | AMC name |
| date | DATE | Quarter end date |
| aum_crore | REAL | AUM in Rs. crore |

---

## 04_monthly_sip_inflows.csv
| Column | Type | Description |
|---|---|---|
| month | TEXT | YYYY-MM format |
| sip_inflow_crore | REAL | Total SIP inflows in Rs. crore |
| active_sip_accounts_crore | REAL | Active SIP accounts in crore |
| new_sip_accounts_lakh | REAL | New SIP registrations in lakh |
| sip_aum_lakh_crore | REAL | Total SIP AUM in Rs. lakh crore |
| yoy_growth_pct | REAL | Year on year growth % |

---

## 05_category_inflows.csv
| Column | Type | Description |
|---|---|---|
| month | TEXT | YYYY-MM format |
| category | TEXT | Fund category (Large Cap / Mid Cap etc.) |
| net_inflow_crore | REAL | Net inflows in Rs. crore |

---

## 06_industry_folio_count.csv
| Column | Type | Description |
|---|---|---|
| period | TEXT | Month/Year period |
| total_folios_crore | REAL | Total MF folios in crore |

---

## 07_scheme_performance.csv
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT | Unique AMFI scheme code |
| scheme_name | TEXT | Fund scheme name |
| return_1yr_pct | REAL | 1 year absolute return % |
| return_3yr_pct | REAL | 3 year CAGR % |
| return_5yr_pct | REAL | 5 year CAGR % |
| benchmark_3yr_pct | REAL | Benchmark 3yr CAGR for comparison |
| alpha | REAL | Return above benchmark |
| beta | REAL | Market sensitivity (1.0 = same as market) |
| sharpe_ratio | REAL | Risk adjusted return (higher = better) |
| sortino_ratio | REAL | Downside risk adjusted return |
| std_dev_ann_pct | REAL | Annualised standard deviation % |
| max_drawdown_pct | REAL | Worst peak to trough decline % |
| morningstar_rating | INT | 1 to 5 star rating |

---

## 08_investor_transactions.csv
| Column | Type | Description |
|---|---|---|
| investor_id | TEXT | Unique investor ID (INV000001 to INV005000) |
| transaction_date | DATE | Date of transaction |
| amfi_code | TEXT | Fund invested in |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INT | Transaction amount in Rs. |
| state | TEXT | Investor state |
| city | TEXT | Investor city |
| city_tier | TEXT | T30 (Top 30 cities) or B30 (Beyond Top 30) |
| age_group | TEXT | 18-25 / 26-35 / 36-45 / 46-55 / 56+ |
| gender | TEXT | Male / Female |
| annual_income_lakh | REAL | Annual income in Rs. lakh |
| payment_mode | TEXT | UPI / Net Banking / Mandate / Cheque |
| kyc_status | TEXT | Verified / Pending |

---

## 09_portfolio_holdings.csv
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT | Fund scheme code |
| stock_symbol | TEXT | NSE stock symbol |
| stock_name | TEXT | Full company name |
| sector | TEXT | Industry sector (Banking / IT / Pharma etc.) |
| weight_pct | REAL | Portfolio weight % |
| market_value_cr | REAL | Market value in Rs. crore |
| current_price_inr | REAL | Current stock price in Rs. |
| portfolio_date | DATE | Holdings as of date |

---

## 10_benchmark_indices.csv
| Column | Type | Description |
|---|---|---|
| date | DATE | Trading date |
| index_name | TEXT | Nifty50 / Nifty100 / BSE SmallCap etc. |
| close_value | REAL | Closing index value |