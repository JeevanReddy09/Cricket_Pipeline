-- models/format_growth_analysis.sql

WITH yearly_format_counts AS (
    SELECT
        EXTRACT(YEAR FROM match_date) AS match_year,
        match_type_detail AS format,
        COUNT(*) AS matches_played
    FROM
        {{ ref('stg_cricket_matches') }}
    WHERE
        match_date IS NOT NULL
        AND match_type_detail IS NOT NULL
    GROUP BY
        1, 2
),

format_trends AS (
    SELECT
        match_year,
        format,
        matches_played,
        LAG(matches_played) OVER (
            PARTITION BY format 
            ORDER BY match_year
        ) AS previous_year_matches
    FROM
        yearly_format_counts
)

SELECT
    match_year,
    format,
    matches_played,
    previous_year_matches,
    CASE 
        WHEN previous_year_matches IS NULL THEN NULL
        ELSE ROUND(
            (matches_played - previous_year_matches) * 100.0 / previous_year_matches, 2
        )
    END AS growth_rate_percent
FROM
    format_trends
ORDER BY
    match_year DESC, matches_played DESC
