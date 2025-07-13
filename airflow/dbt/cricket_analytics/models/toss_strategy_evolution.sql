-- models/toss_strategy_evolution.sql

WITH yearly_toss_counts AS (
    SELECT
        EXTRACT(YEAR FROM match_date) AS match_year,
        toss_decision,
        COUNT(*) AS decision_count
    FROM
        {{ ref('stg_cricket_matches') }}
    WHERE
        match_date IS NOT NULL
        AND toss_decision IS NOT NULL
    GROUP BY
        1, 2
),

yearly_totals AS (
    SELECT
        match_year,
        SUM(decision_count) AS total_decisions
    FROM
        yearly_toss_counts
    GROUP BY
        1
)

SELECT
    ytc.match_year,
    ytc.toss_decision,
    ytc.decision_count,
    ROUND(
        ytc.decision_count * 100.0 / yt.total_decisions, 2
    ) AS percentage_of_year
FROM
    yearly_toss_counts ytc
JOIN
    yearly_totals yt ON ytc.match_year = yt.match_year
ORDER BY
    ytc.match_year DESC, ytc.decision_count DESC
