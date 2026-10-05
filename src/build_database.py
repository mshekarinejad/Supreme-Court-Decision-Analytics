"""Build a SQLite database from the processed Supreme Court datasets."""

import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DATABASE = ROOT / "data" / "supreme_court_analytics.db"


def main() -> None:
    tables = {
        "justice_votes": "justice_votes_clean.csv",
        "cases": "cases_summary.csv",
        "justice_summary": "justice_summary.csv",
        "justice_alignment": "justice_alignment.csv",
        "issue_area_summary": "issue_area_summary.csv",
    }

    with sqlite3.connect(DATABASE) as connection:
        for table_name, filename in tables.items():
            frame = pd.read_csv(PROCESSED / filename)
            frame.to_sql(table_name, connection, if_exists="replace", index=False)

        connection.execute("CREATE INDEX IF NOT EXISTS idx_cases_term ON cases(term)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_cases_issue_area ON cases(issueArea)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_votes_justice ON justice_votes(justiceName)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_votes_case ON justice_votes(caseId)")

    print(f"Created SQLite database: {DATABASE}")


if __name__ == "__main__":
    main()
