# Project Plan: Soccer Match Outcomes and Pre-Match Expectations

## Overview

For this project, I want to work with soccer data because it is a topic I already understand well and genuinely enjoy. The goal is to combine two soccer datasets and study matches where the expected result did not happen.

The first dataset will come from StatsBomb Open Data and will provide detailed match and event information. The second dataset will come from FiveThirtyEight’s Soccer Power Index data and will provide pre-match team ratings and win probabilities.

The main idea is to compare what was expected before a match with what actually happened during the match. I am especially interested in games where the favorite did not win. I want to see whether factors such as shots, expected goals, possession, and passing help explain those results.

The project will focus on one competition and season that appears in both datasets. My first choice is La Liga 2020/2021, but I will confirm the overlap after downloading and inspecting the data.

## Team

I will complete this project individually. The course staff has already approved me to work alone.

I will be responsible for collecting the data, cleaning it, combining the datasets, completing the analysis, creating visualizations, and writing the final report.

## Research Questions

The project will focus on the following questions:

1. How often did the team favored by the FiveThirtyEight SPI probabilities actually win?
2. What match statistics were most different between expected wins and unexpected results?
3. Did factors such as expected goals, number of shots, possession, or passing help explain why the favorite failed to win?
4. Which teams most often performed better or worse than their pre-match expectations?

For this project, I will initially define the favorite as the team with the higher pre-match win probability. An unexpected result will be a match where that team either drew or lost.

## Datasets

### StatsBomb Open Data

StatsBomb Open Data provides soccer data through its official GitHub repository. The data is stored mainly in JSON files.

The dataset includes information about competitions, seasons, matches, lineups, and individual events during matches. Some of the fields I expect to use are:

- match ID;
- match date;
- home and away teams;
- final score;
- shots;
- shot outcomes;
- expected goals;
- passes;
- possession information;
- player and team names.

This dataset will help explain what happened during each match.

### FiveThirtyEight Soccer Power Index Data

The FiveThirtyEight soccer dataset includes historical club soccer forecasts and match results. It is stored in CSV format.

Some of the fields I expect to use are:

- league;
- season;
- match date;
- home and away teams;
- team SPI ratings;
- projected goals;
- home-win, draw, and away-win probabilities;
- final score.

This dataset will provide the pre-match expectations that I can compare with the actual result and the StatsBomb event data.

### Combining the Datasets

The datasets do not appear to share the same match ID, so I will likely match records using:

- match date;
- home team;
- away team.

Team names may be written differently in the two datasets, so I may need to create a small team-name mapping table. I will try exact matching first and only use fuzzy matching for records that are still unmatched.

I will also keep track of which matches were linked successfully and which were not.

## Data Collection and Organization

The project repository will separate raw data from cleaned and processed data. A possible structure is:

```text
data/
  raw/
  processed/
scripts/
notebooks/
outputs/
ProjectPlan.md
README.md
requirements.txt
```

The raw files will not be overwritten. Cleaned and combined datasets will be saved separately.

I will use Python scripts to download or load the data, clean it, combine it, and create the final outputs. I will also record the data sources and retrieval dates.

## Cleaning and Data Quality

Before analysis, I will inspect both datasets for:

- missing values;
- duplicate records;
- inconsistent team names;
- incorrect data types;
- invalid dates;
- missing scores or probabilities;
- unmatched matches after integration.

I will standardize dates, team names, and missing values. I will also compare final scores across both datasets to make sure the linked matches are correct.

For the StatsBomb data, I will create match-level statistics from the event records. These may include:

- total shots;
- shots on target;
- expected goals;
- pass completion;
- possession or a possession-related measure.

The final set of variables may change depending on what is available and how difficult it is to calculate them correctly.

## Ethical and Legal Considerations

The project uses public data about professional soccer matches. It does not appear to contain sensitive personal information.

I will credit both StatsBomb and FiveThirtyEight in the repository and final report. I will also follow the licensing and attribution requirements listed by the original sources.

I will be careful not to treat probability as certainty. A favorite losing does not automatically mean the forecast was bad, since the model still gives some probability to a draw or loss.

## Reproducibility

The goal is for the project to run from start to finish without manually editing the data each time.

I plan to create a main Python script that:

1. loads the raw data;
2. cleans and standardizes the files;
3. combines matching records;
4. creates match-level statistics;
5. saves the final dataset;
6. creates tables and visualizations.

The repository will include a `requirements.txt` file and instructions in the README explaining how to run the project.

## Timeline

| Task | Planned Time |
|---|---|
| Confirm datasets and competition | Day 1 |
| Download and inspect the data | Days 2–3 |
| Clean both datasets | Days 3–5 |
| Create team-name mappings | Days 5–6 |
| Combine the datasets | Days 6–8 |
| Create match-level statistics | Days 8–10 |
| Complete the analysis | Days 10–12 |
| Create visualizations | Days 12–13 |
| Write and revise the final report | Days 13–15 |

## Constraints

The biggest possible issue is that the two datasets may not cover all of the same matches. The final sample will depend on how many matches can be linked correctly.

Other possible challenges include different team names, missing values, large JSON files, and the difficulty of converting event-level data into match-level statistics.

Since I am completing the project alone, I will also need to keep the scope realistic. I would rather answer a few clear questions well than create an overly large project that is difficult to finish or reproduce.

## Gaps

I have not yet confirmed the exact number of overlapping matches between the two datasets. I will do that during the first data-inspection step.

I also have not finalized every match statistic that will be included. The final choices will depend on the quality and structure of the StatsBomb event data.

If La Liga 2020/2021 does not have enough overlap, I will choose another competition and season that appears in both datasets while keeping the same general research questions.

## References

- StatsBomb Open Data: https://github.com/statsbomb/open-data
- FiveThirtyEight Data Repository: https://github.com/fivethirtyeight/data
