-- models/staging/stg_cricket_matches.sql

SELECT
    -- Standardize and clean the raw data
    CAST(match_date AS DATE) as match_date,
    TRIM(match_type) as match_type,
    TRIM(winner) as winning_team,
    TRIM(team_1) as team_one,
    TRIM(team_2) as team_two,
    TRIM(venue) as venue,
    TRIM(city) as city,
    TRIM(toss_decision) as toss_decision,
    TRIM(toss_winner) as toss_winner,
    TRIM(result) as result,
    SAFE_CAST(win_by_runs AS INT64) as win_by_runs,
    SAFE_CAST(win_by_wickets AS INT64) as win_by_wickets,
    TRIM(player_of_match) as player_of_match,
    TRIM(overs) as overs,
    TRIM(event_name) as event_name,
    TRIM(gender) as gender
FROM {{ source('cricket_raw', 'matches') }}
WHERE match_date IS NOT NULL
