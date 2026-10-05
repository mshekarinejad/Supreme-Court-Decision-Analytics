# U.S. Supreme Court Decision Analytics (1946–2024)

An end-to-end legal data analytics project examining voting patterns in U.S.
Supreme Court decisions from 1946 through 2024. I used Python and SQLite to
prepare the data, then built an interactive Tableau dashboard to explore
majority participation, 5–4 decisions, issue-area patterns, and voting
alignment between justices.

## Tableau dashboard

The dashboard contains four views:

- **5–4 decisions by term:** the number of closely divided decisions each term.
- **5–4 decision rate by legal issue area:** the share of cases in each issue area decided 5–4.
- **Highest vs. lowest justice majority-vote rates:** the five justices most and least often joining the Court's majority, across each justice's own service period.
- **Highest vs. lowest justice-pair voting alignment:** the five most and least aligned justice pairs. Each pair was compared across at least 178 shared cases.

The packaged Tableau workbook is available as `Supreme_Court_Decision_Analytics.twbx`.

## Questions explored

- Which issue areas produce the highest share of 5–4 decisions?
- How has the frequency of 5–4 decisions changed over time?
- Which justices most often voted with the Court's majority?
- Which pairs of justices most often aligned in the same majority or dissent coalition?

## Research framing

This project treats a 5–4 decision as a descriptive indicator of a closely
divided Court. It does **not** assume that every 5–4 decision has the same
legal or political meaning. The analysis asks where and when close divisions
appeared in the data, then compares voting patterns without drawing causal
conclusions about ideology, doctrine, or individual judicial quality.

## Methodology

The raw justice-centered dataset contains one row for each justice's vote in
a case. Python first standardizes the relevant fields and creates a
case-level table with one row per `caseId`; this prevents a single case from
being counted once for every participating justice. A case is marked as 5–4
only when its final vote totals are exactly five votes to four.

The project then produces separate summaries for legal issue areas, justices,
and justice pairs:

- **Issue-area 5–4 rate** = 5–4 cases in an issue area / all cases in that issue area.
- **Justice majority-vote rate** = cases in which a justice joined the Court majority / cases that justice voted in.
- **Justice-pair alignment rate** = shared cases in which both justices joined the same majority or dissent coalition / shared cases compared.

SQLite stores the prepared tables and the included SQL queries reproduce the
headline calculations. Tableau connects to the processed CSV files to create
the dashboard.

## Selected findings

- The number of 5–4 decisions varied substantially by term. The highest count
  in this dataset was **44 decisions in the 1986 term**; other high-count
  terms include 1989 (39) and 1985 (37).
- The **First Amendment** had the highest 5–4 decision rate among the listed
  issue areas at **23.3%** (165 of 707 cases). Criminal Procedure had a
  lower rate (**20.3%**) but a much larger case volume (2,103 cases).
- Justice majority vote rates describe how often a justice joined the final
  Court majority during that justice's service period. They should not be
  interpreted as measures of correctness, influence, or ideology.
- The justice pair view highlights the most and least aligned pairs in the
  data. Every pair in the prepared dataset shares at least 178 cases, avoiding
  comparisons based on only a few overlapping decisions.

## Interpretation and limitations

- This is a descriptive analysis, not a causal claim about why the Court was
  divided in a particular term or issue area.
- A justice's rate reflects the cases and Court composition during that
  justice's own service period; direct comparisons across eras require care.
- Pairwise alignment identifies whether two justices joined the same
  majority/ dissent coalition. It does not show whether they joined the same
  opinion, used the same reasoning, or agreed on every legal question.
- SCDB coding choices and case classifications are the basis of the analysis,
  readers should consult the SCDB documentation for full variable definitions.

## Data source

The raw data is the Justice-Centered, Citation-Organized CSV from the
[Supreme Court Database (SCDB), 2025 Release 01](https://scdb.la.psu.edu/data/2025-release-01/).
It includes terms 1946–2024. Each row represents one justice's vote in a
Supreme Court dispute.

SCDB defines `majority = 2` as a vote with the majority and `majority = 1`
as a dissent. Pairwise alignment in this project measures whether two
justices were in the same majority/dissent coalition; it does not determine
whether they agreed with the same legal reasoning.

## Project structure

```text
data/raw/        Original SCDB download
data/processed/  Analysis-ready datasets created by the script
src/             Python data-preparation code
sql/             Reusable SQLite analysis queries
Supreme_Court_Decision_Analytics.twbx  Packaged Tableau dashboard
dashboard.png    Dashboard preview used above
```

## Run the preparation script

```bash
pip install -r requirements.txt
python src/prepare_data.py
```

## SQL analysis

The project includes a portable SQLite database and five reusable SQL queries
in `sql/analysis_queries.sql`. Create the database after preparing the data:

```bash
python src/build_database.py
```

Open `data/supreme_court_analytics.db` in DB Browser for SQLite or another
SQLite client, then run the queries in `sql/analysis_queries.sql`.

## Citation

Harold J. Spaeth, Lee Epstein, Michael J. Nelson, Andrew D. Martin, et al.
2025 Supreme Court Database, Version 2025 Release 1.
