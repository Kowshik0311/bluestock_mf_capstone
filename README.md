# Bluestock Fintech — Mutual Fund Analytics Platform

## Project Overview
An end-to-end Mutual Fund Analytics Platform built during Data Analyst Internship at Bluestock Fintech (Cohort 2025). Analyzes 40 mutual fund schemes across 10 fund houses using real AMFI India data.

## Tech Stack
- Python 3.12 (Pandas, NumPy, Matplotlib, Seaborn, Plotly, SciPy)
- SQLite (via SQLAlchemy)
- Tableau Public (Dashboard)
- Git + GitHub

## Project Structure
bluestock_mf_capstone/
├── data/
│   ├── raw/           ← Original CSV + live NAV files
│   ├── processed/     ← Cleaned datasets + metrics
│   └── db/            ← SQLite database
├── notebooks/
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
├── scripts/
│   ├── data_ingestion.py
│   ├── live_nav_fetch.py
│   ├── data_cleaning.py
│   └── create_database.py
├── sql/
│   └── schema.sql
├── reports/
│   └── Final_Report.md
└── README.md

## How to Run
1. Clone the repo
git clone https://github.com/Kowshik0311/bluestock_mf_capstone.git
cd bluestock_mf_capstone

2. Install dependencies
pip install -r requirements.txt

3. Run data ingestion
python scripts/data_ingestion.py
python scripts/live_nav_fetch.py

4. Run data cleaning
python scripts/data_cleaning.py

5. Create database
python scripts/create_database.py

6. Open notebooks in VS Code or Jupyter and run in order

## Key Findings
1. SIP inflows grew 2.5x from Rs.12,000 Cr to Rs.31,002 Cr (2022–2026)
2. SBI MF dominates AUM at Rs.12.5 lakh crore
3. Industry folios doubled from 13.3 Cr to 26 Cr in 3 years
4. ICICI Pru Liquid Fund has highest Sharpe ratio of 7.7
5. All top 5 funds outperformed Nifty 50 and Nifty 100 over 3 years
6. Banking (19.2%) and IT (13.4%) dominate equity fund portfolios
7. 26–35 age group drives most mutual fund transactions
8. T30 cities contribute 65.9% of total transaction value

## Dashboard
Tableau Public: https://public.tableau.com/app/profile/k.v.kowshik.athreya/viz/Bluestock_MF_Dashboard/Dashboard1

## Data Sources
- AMFI India (amfiindia.com)
- mfapi.in (live NAV API)
- NSE/BSE benchmark indices

## Author
**Kowshik Athreya**
- GitHub: github.com/kowshik0311
- LinkedIn: linkedin.com/in/kowshik-athreya
- Email: kowshikathreya2004@gmail.com

## License
For educational purposes only. Data sourced from publicly available AMFI India records.