# Data Dictionary

## data/raw/statsbomb_matches_curated.csv

| Field | Type | Description |
|---|---|---|
| match_id | integer | StatsBomb match identifier |
| date | date | Match date |
| home_team | string | StatsBomb home-team name |
| away_team | string | StatsBomb away-team name |
| home_score | integer | Full-time home score |
| away_score | integer | Full-time away score |
| match_week | integer | La Liga match week |

## data/raw/footballcsv_matches_curated.csv

| Field | Type | Description |
|---|---|---|
| date | date | Match date |
| team1 | string | Home team in football.csv naming |
| FT | string | Full-time score as home-away |
| HT | string | Half-time score as home-away |
| team2 | string | Away team in football.csv naming |

## data/processed/integrated_matches.csv

The processed file includes all fields above plus normalized team keys, merge status, a score-agreement flag, Barcelona goals for/against, venue, final result, half-time goals for/against, and half-time state.
