-- models/venue_activity_summary.sql

SELECT
    venue,
    city,
    COUNT(*) AS total_matches,
    MIN(match_date) AS first_match,
    MAX(match_date) AS last_match,
    COUNT(DISTINCT EXTRACT(YEAR FROM match_date)) AS active_years,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2
    ) AS percentage_of_all_matches
FROM
    {{ ref('stg_cricket_matches') }}
WHERE
    venue IS NOT NULL
    AND match_date IS NOT NULL
GROUP BY
    1, 2
HAVING
    COUNT(*) >= 5  -- Only venues with meaningful activity
ORDER BY
    total_matches DESC
