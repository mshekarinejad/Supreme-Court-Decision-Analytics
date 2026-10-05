-- 1. Five-to-four decisions by Supreme Court term.
SELECT
    term,
    COUNT(*) AS total_cases,
    SUM(is_five_to_four) AS five_to_four_cases,
    ROUND(100.0 * SUM(is_five_to_four) / COUNT(*), 1) AS five_to_four_pct
FROM cases
GROUP BY term
ORDER BY term;

-- 2. Issue areas with the largest share of five-to-four decisions.
SELECT
    issue_area_name,
    COUNT(*) AS total_cases,
    SUM(is_five_to_four) AS five_to_four_cases,
    ROUND(100.0 * SUM(is_five_to_four) / COUNT(*), 1) AS five_to_four_pct
FROM cases
WHERE issue_area_name IS NOT NULL
GROUP BY issue_area_name
HAVING COUNT(*) >= 50
ORDER BY five_to_four_pct DESC, total_cases DESC;

-- 3. Justices who most often voted with the Court majority.
SELECT
    justiceName,
    cases_voted,
    majority_votes,
    ROUND(100.0 * majority_rate, 1) AS majority_vote_pct
FROM justice_summary
WHERE cases_voted >= 100
ORDER BY majority_rate DESC, cases_voted DESC;

-- 4. Justice pairs with the highest majority/dissent alignment.
SELECT
    justice_a,
    justice_b,
    cases_compared,
    ROUND(100.0 * alignment_rate, 1) AS alignment_pct
FROM justice_alignment
WHERE cases_compared >= 100
ORDER BY alignment_rate DESC, cases_compared DESC;

-- 5. Five-to-four decisions by issue area in the most recent 20 terms.
SELECT
    issue_area_name,
    COUNT(*) AS total_cases,
    SUM(is_five_to_four) AS five_to_four_cases,
    ROUND(100.0 * SUM(is_five_to_four) / COUNT(*), 1) AS five_to_four_pct
FROM cases
WHERE term >= 2005 AND issue_area_name IS NOT NULL
GROUP BY issue_area_name
ORDER BY five_to_four_pct DESC, total_cases DESC;
