"""Prepare SCDB justice vote data for the project."""

from itertools import combinations
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "SCDB_2025_01_justiceCentered_Citation.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

ISSUE_AREAS = {
    1: "Criminal Procedure", 2: "Civil Rights", 3: "First Amendment",
    4: "Due Process", 5: "Privacy", 6: "Attorneys", 7: "Unions",
    8: "Economic Activity", 9: "Judicial Power", 10: "Federal Taxation",
    11: "Miscellaneous", 12: "Private Action", 13: "Federalism",
    14: "Interstate Relations",
}


def build_agreement_table(votes: pd.DataFrame) -> pd.DataFrame:
    """Calculate pairwise majority/dissent alignment within the same case.

    SCDB's ``majority`` field is 2 for a justice voting with the majority and
    1 for a dissent. This measures alignment with the Court's coalition, not
    agreement with a particular opinion's legal reasoning.
    """
    rows = []
    valid = votes.loc[votes["majority"].isin([1, 2]), ["caseId", "justiceName", "majority"]]

    for _, case_votes in valid.groupby("caseId"):
        case_votes = case_votes.drop_duplicates("justiceName")
        for left, right in combinations(case_votes.itertuples(index=False), 2):
            justice_a, justice_b = sorted((left.justiceName, right.justiceName))
            rows.append({
                "justice_a": justice_a,
                "justice_b": justice_b,
                "aligned": int(left.majority == right.majority),
            })

    pairs = pd.DataFrame(rows)
    return (
        pairs.groupby(["justice_a", "justice_b"], as_index=False)
        .agg(cases_compared=("aligned", "size"), aligned_cases=("aligned", "sum"))
        .assign(alignment_rate=lambda x: x["aligned_cases"] / x["cases_compared"])
        .sort_values(["alignment_rate", "cases_compared"], ascending=[False, False])
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    votes = pd.read_csv(RAW_PATH, encoding="latin-1", low_memory=False)
    votes["dateDecision"] = pd.to_datetime(votes["dateDecision"], errors="coerce")
    votes["issueArea"] = pd.to_numeric(votes["issueArea"], errors="coerce")
    votes["issue_area_name"] = votes["issueArea"].map(ISSUE_AREAS)
    votes["majority"] = pd.to_numeric(votes["majority"], errors="coerce")
    votes["majVotes"] = pd.to_numeric(votes["majVotes"], errors="coerce")
    votes["minVotes"] = pd.to_numeric(votes["minVotes"], errors="coerce")

    clean_votes = votes.loc[
        votes["justiceName"].notna(),
        ["caseId", "dateDecision", "term", "naturalCourt", "chief", "caseName",
         "issueArea", "issue_area_name", "majVotes", "minVotes", "justice",
         "justiceName", "vote", "direction", "majority"],
    ].copy()
    clean_votes.to_csv(OUTPUT_DIR / "justice_votes_clean.csv", index=False)

    cases = (
        clean_votes.sort_values("caseId").drop_duplicates("caseId")
        .assign(is_five_to_four=lambda x: (x["majVotes"] == 5) & (x["minVotes"] == 4))
    )
    cases.to_csv(OUTPUT_DIR / "cases_summary.csv", index=False)

    justice_summary = (
        clean_votes.loc[clean_votes["majority"].isin([1, 2])]
        .groupby("justiceName", as_index=False)
        .agg(cases_voted=("caseId", "nunique"), majority_votes=("majority", lambda x: (x == 2).sum()))
        .assign(majority_rate=lambda x: x["majority_votes"] / x["cases_voted"])
        .sort_values("majority_rate", ascending=False)
    )
    justice_summary.to_csv(OUTPUT_DIR / "justice_summary.csv", index=False)

    build_agreement_table(clean_votes).to_csv(OUTPUT_DIR / "justice_alignment.csv", index=False)

    issue_summary = (
        cases.groupby(["issueArea", "issue_area_name"], dropna=False, as_index=False)
        .agg(cases=("caseId", "nunique"), five_to_four_cases=("is_five_to_four", "sum"))
        .assign(five_to_four_rate=lambda x: x["five_to_four_cases"] / x["cases"])
        .sort_values("cases", ascending=False)
    )
    issue_summary.to_csv(OUTPUT_DIR / "issue_area_summary.csv", index=False)
    print(f"Created analysis-ready files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
