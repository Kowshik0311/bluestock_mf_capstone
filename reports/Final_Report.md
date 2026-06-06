# Bluestock Fintech — Mutual Fund Analytics Platform
## Final Report | June 2026
**Prepared by:** Kowshik Athreya | Data Analyst Intern | Bluestock Fintech Pvt. Ltd.

---

## 1. Executive Summary
This project built an end-to-end Mutual Fund Analytics Platform analyzing 40 schemes across 10 fund houses using real AMFI data. Key findings include SBI MF dominating with Rs.12.5L Cr AUM, SIP inflows hitting all-time high of Rs.31,002 Cr in Dec 2025, and ICICI Pru Liquid Fund achieving highest Sharpe ratio of 7.7. All top 5 funds outperformed Nifty 50 and Nifty 100 benchmarks over 3 years.

---

## 2. Problem Statement
Indian mutual fund data is fragmented across multiple sources. Investors lack unified analytics to make data-driven fund selection decisions. This project solves:
- Data fragmentation — unified ETL pipeline
- Performance comparison gap — risk-adjusted metrics dashboard
- No benchmark tracking — NAV vs Nifty comparison
- Investor behaviour blind spot — demographic and geographic analysis

---

## 3. Data Sources
- 10 CSV datasets provided by Bluestock Fintech (AMFI sourced)
- Live NAV data from mfapi.in API (6 schemes, 3000+ records each)
- Benchmark indices: Nifty 50, Nifty 100, BSE SmallCap

---

## 4. System Architecture
Extract (AMFI CSVs + mfapi.in) → Transform (Pandas cleaning) → Load (SQLite) → Analyse (Jupyter) → Visualise (Tableau)

---

## 5. ETL Pipeline
- Loaded 10 raw CSVs using Pandas
- Cleaned all datasets — nulls, duplicates, forward-fill for NAV weekends/holidays
- Validated AMFI codes — 40/40 match
- Stored in SQLite database with 14 tables

---

## 6. Key EDA Findings
1. SIP inflows grew 2.5x from Rs.12,000 Cr to Rs.31,002 Cr (2022–2026)
2. SBI MF dominates AUM at Rs.12.5 lakh crore
3. 26–35 age group drives most transactions (13,000+)
4. Industry folios doubled from 13.3 Cr to 26 Cr in 3 years
5. Banking (19.2%) and IT (13.4%) dominate equity fund portfolios
6. T30 cities contribute 65.9% of total transaction value
7. Liquid funds receive highest monthly inflows consistently
8. HDFC, ICICI, Kotak and Nippon are highly correlated (0.74–0.89)

---

## 7. Performance Metrics
| Metric | Top Fund | Value |
|---|---|---|
| CAGR | SBI Bluechip | Highest among 6 |
| Sharpe Ratio | ICICI Pru Liquid | 7.7 |
| Lowest VaR | ICICI Pru Liquid | Minimal daily loss |
| Best Scorecard | Kotak Bluechip | Score 100 |

All top 5 funds outperformed Nifty 50 and Nifty 100 over 3 years.

---

## 8. Advanced Analytics
- VaR (95%) — liquid funds safest with minimal daily loss risk
- Rolling Sharpe — equity funds dipped below 1 during 2024 corrections
- Cohort analysis — 2024 cohort investors have highest average SIP amounts
- SIP continuity — significant investors have gaps > 35 days, at-risk of stopping
- Fund recommender — built for Low/Moderate/High risk investors
- Sector HHI — Banking most concentrated sector across equity funds

---

## 9. Dashboard
Built using Tableau Public with 4 pages:
- Industry Overview
- Fund Performance
- Investor Analytics
- SIP Trends

---

## 10. Recommendations
1. Investors seeking stability should choose liquid/gilt funds
2. Young investors (26–35) should focus on Large Cap for long-term wealth
3. Diversify across low-correlated funds (Axis + SBI Bluechip combination)
4. B30 city investors represent significant untapped market opportunity
5. SIP investors with gaps > 35 days need re-engagement campaigns

---

## 11. Limitations
- Live NAV limited to 6 schemes
- Investor transaction data is simulated
- Alpha/Beta calculation had limited common dates with benchmark

---

## 12. GitHub Repository
github.com/Kowshik0311/bluestock_mf_capstone