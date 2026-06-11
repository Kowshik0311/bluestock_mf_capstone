"""
Bluestock Fintech — Mutual Fund Analytics Platform
=================================================
Script  : run_pipeline.py
Purpose : Master execution script — runs the complete ETL pipeline
          in the correct order with status reporting
Author  : Kowshik Athreya
Date    : June 2026

Usage:
    python run_pipeline.py

Pipeline Steps:
    1. Data Ingestion  — load 10 CSVs + fetch live NAV from mfapi.in
    2. Data Cleaning   — clean and validate all datasets
    3. Database Load   — create SQLite DB and load all tables
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ─── Path Configuration ───────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR / "scripts"


def run_script(script_name: str) -> bool:
    """
    Execute a Python script and report success or failure.

    Args:
        script_name: Name of the script file inside scripts/ folder

    Returns:
        True if script ran successfully, False otherwise
    """
    script_path = SCRIPTS_DIR / script_name
    print(f"\n{'='*60}")
    print(f"  Running: {script_name}")
    print(f"  Time   : {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=False
    )

    if result.returncode == 0:
        print(f"\n  ✅ {script_name} completed successfully!")
        return True
    else:
        print(f"\n  ❌ {script_name} failed with error code {result.returncode}")
        return False


def main():
    """
    Main pipeline executor.
    Runs all ETL scripts in order and reports final status.
    """
    print("\n" + "="*60)
    print("  BLUESTOCK FINTECH — MUTUAL FUND ANALYTICS PLATFORM")
    print("  ETL Pipeline Starting...")
    print(f"  Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # Define pipeline steps in order
    pipeline = [
        "data_ingestion.py",
        "live_nav_fetch.py",
        "data_cleaning.py",
        "create_database.py",
    ]

    results = {}

    # Execute each step
    for script in pipeline:
        success = run_script(script)
        results[script] = success

        # Stop pipeline if a critical step fails
        if not success:
            print(f"\n⛔ Pipeline stopped at {script}")
            print("Fix the error and re-run run_pipeline.py")
            break

    # Final summary
    print("\n" + "="*60)
    print("  PIPELINE EXECUTION SUMMARY")
    print("="*60)
    for script, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {status} — {script}")

    total    = len(results)
    passed   = sum(results.values())
    failed   = total - passed

    print(f"\n  Total  : {total}")
    print(f"  Passed : {passed}")
    print(f"  Failed : {failed}")
    print(f"\n  End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if failed == 0:
        print("\n✅ Full pipeline completed successfully!")
        print("   You can now open the notebooks for analysis.")
        print("   Dashboard: https://public.tableau.com/app/profile/k.v.kowshik.athreya/viz/Bluestock_MF_Dashboard/Dashboard1")
    else:
        print("\n⚠ Pipeline completed with errors. Check logs above.")

    print("="*60)


if __name__ == "__main__":
    main()