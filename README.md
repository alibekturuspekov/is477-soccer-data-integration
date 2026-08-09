# Integrating La Liga Match Data Across Two Public Soccer Sources

## Contributors

- Alibek Turuspekov

## Summary

For this project, I wanted to work with soccer data because it is a topic I already understand and follow closely. My original project plan was more ambitious: I wanted to combine StatsBomb event data with FiveThirtyEight Soccer Power Index forecasts and study games where the favorite did not win. As I started putting the final workflow together, I ran into a reproducibility problem with the FiveThirtyEight source. The historical dataset is still documented, but the original live CSV endpoint I planned to use was no longer a stable way to obtain the file. Instead of building the final submission around an unreliable download or a random mirror, I changed the second source to the public football.csv cache of Football-Data.

The final project therefore focuses more directly on the data-management side of the course. I integrate two independently maintained representations of La Liga 2020/2021 matches: StatsBomb Open Data and football.csv. StatsBomb contributes a persistent match identifier, match week, standardized team names, and the final score. football.csv contributes its own team naming conventions together with full-time and half-time scores. The two sources do not share a match ID, so they have to be connected through date and normalized home/away team names.

I created a 19-match Barcelona-centered sample from the season so that I could complete and verify the entire workflow rather than leave a larger pipeline partially finished. This sample contains matches from September 2020 through May 2021 and includes home and away games, wins, draws, and losses.

The main questions became: Can the two sources be integrated reliably despite different team naming conventions? Do their final scores agree after integration? What does the additional half-time information from football.csv show about Barcelona's results in the integrated sample?

The integration linked all **19** records in the curated sample and the final scores agreed for **100%** of linked matches. Barcelona recorded **11 wins, 4 draws, and 4 losses**, scoring **42** goals and allowing **20**. The half-time data also showed that Barcelona was behind at half time in **4** matches and recovered to win only **1** of them. At the same time, being ahead at half time did not guarantee a win: **3** matches in the sample ended without a Barcelona victory after Barcelona had led at the break.

The main result of the project is less about making a strong causal claim about soccer and more about showing a transparent and reproducible integration process. The final repository preserves raw curated inputs, a documented name-normalization rule, an integrated dataset, quality checks, output tables, visualizations, metadata, and a `run_all.py` workflow.

## Data Profile

### StatsBomb Open Data

The first source is StatsBomb Open Data. StatsBomb publishes selected soccer data in a public GitHub repository as JSON files. Competition and season information is stored separately from matches, while match files contain metadata such as match ID, date, home and away teams, score, match week, stadium, referee, and other fields.

For La Liga 2020/2021, the source uses competition ID `11` and season ID `90`. The full source is a nested JSON file. For this project, I created a smaller tabular extract containing only the fields needed for integration:

- `match_id`
- `date`
- `home_team`
- `away_team`
- `home_score`
- `away_score`
- `match_week`

The input used by the workflow is stored at:

`data/raw/statsbomb_matches_curated.csv`

The original source URL and provenance information are documented in `metadata/source_notes.md`.

StatsBomb asks users who publish or share analysis based on its open data to identify StatsBomb as the data source. I therefore keep the source clearly identified in this README and in the metadata documentation.

### football.csv / Football-Data

The second source is the `footballcsv/cache.footballdata` GitHub repository. It provides a public cache of football-data.co.uk match files and distributes the cache under CC0-1.0. Unlike StatsBomb's nested JSON structure, this data is organized as a simple CSV with one match per row.

For this project I use the Spanish top-division file for the 2020/2021 season. The curated input keeps:

- `date`
- `team1`
- `FT`
- `HT`
- `team2`

Here, `FT` is the full-time score and `HT` is the half-time score.

The input used by the workflow is stored at:

`data/raw/footballcsv_matches_curated.csv`

The two sources complement each other. StatsBomb supplies its match identifier and match-week metadata. football.csv supplies the half-time score and provides an independent full-time score that can be used as a cross-source quality check.

### Storage and Organization

The repository separates data by lifecycle stage:

```text
data/
  raw/
  processed/
outputs/
  tables/
  figures/
scripts/
metadata/
```

The files in `data/raw/` are not overwritten by the workflow. `scripts/clean_integrate.py` reads those inputs and writes a new file to `data/processed/integrated_matches.csv`. Analysis results are written separately to `outputs/`.

This structure follows the course idea of keeping acquisition/source data separate from transformed data and final results.

### Ethical and Legal Issues

The project uses public professional soccer match records. The selected fields do not contain confidential or sensitive personal data.

The main legal and policy issues are attribution, licensing, and provenance. StatsBomb has an attribution requirement for published analysis using its open data. The football.csv cache is marked CC0-1.0. I did not use Kaggle because the course project specifically emphasizes traceable data provenance and licensing.

## Data Quality

I assessed the datasets for completeness, duplicates, validity, consistency, and integration success.

The curated StatsBomb input has 19 rows and no missing values in the fields used by this project. The curated football.csv input also has 19 rows and no missing values. Neither source contains duplicate rows in the curated sample.

The most important quality test was integration coverage. The two sources do not use the same team names in every case. For example, the football.csv source uses names such as `Alaves`, `Betis`, `Celta`, `Levante`, `Ath Madrid`, and `Ath Bilbao`, while StatsBomb uses `Deportivo Alavés`, `Real Betis`, `Celta Vigo`, `Levante UD`, `Atlético Madrid`, and `Athletic Club`.

Before cleaning, these differences prevent a direct equality join. After normalization and the alias map, all 19 StatsBomb sample records matched a football.csv record using date, normalized home team, and normalized away team. This produced an integration rate of 100% for the curated sample.

I also used final score as an independent consistency test after matching. StatsBomb stores home and away score as separate numeric fields, while football.csv stores the result as a string such as `2-1`. After converting the StatsBomb score to the same representation, all 19 linked matches agreed on the full-time result.

This does not prove the complete underlying databases are error-free. It only shows that the selected sample is internally consistent on the fields used for integration. A larger project should profile the full season and inspect any unmatched or score-disagreement cases individually.

The generated quality summary is stored in `outputs/tables/data_quality_summary.csv`.

## Data Cleaning

The main cleaning problem was semantic inconsistency in team names. I created `normalize_team()` in `scripts/clean_integrate.py`. The function converts text to lowercase, removes accents, removes punctuation, and standardizes repeated whitespace.

That solves differences such as `Cádiz` versus `Cadiz`, but it does not solve differences where the words themselves are different. For those cases I created a small explicit alias dictionary. Examples include:

- `Alaves` -> `Deportivo Alaves`
- `Betis` -> `Real Betis`
- `Celta` -> `Celta Vigo`
- `Levante` -> `Levante UD`
- `Ath Madrid` -> `Atletico Madrid`
- `Ath Bilbao` -> `Athletic Club`
- `Valladolid` -> `Real Valladolid`

I preferred an explicit alias map to uncontrolled fuzzy matching because the sample is small enough to review manually. This makes every semantic change visible in the code.

Dates from both files are converted to Pandas datetime values before joining. The integration key consists of date, normalized home team, and normalized away team.

After the join, I create several derived fields rather than changing the source fields. These include `score_agrees`, `barca_gf`, `barca_ga`, `venue`, `result`, and `halftime_state`.

This approach preserves the original source columns in the integrated output and makes the transformations easier to inspect. The script writes the cleaned result to `data/processed/integrated_matches.csv`.

## Findings

The first finding is that the integration method worked cleanly for the curated sample. All 19 StatsBomb records linked to one football.csv record, and all linked records had the same full-time score in both sources. This is useful because the two sources were collected and distributed independently and use different schemas and naming conventions.

Within the sample, Barcelona went **11-4-4** across the 19 matches. The team scored **42 goals** and conceded **20**, for a goal difference of **+22**.

There were **8 home matches** and **11 away matches** in the selected records. Barcelona won **4** of the home matches and **7** of the away matches. Because this is a curated sample rather than the full season, I do not treat the difference as evidence of a general home/away effect.

The half-time field from football.csv adds information that was not present in my StatsBomb match-level extract. Barcelona was behind at half time in **4** matches. Only **1** of those became wins, the 3-2 away victory against Real Betis on February 7, 2021. The sample also contains examples in the opposite direction: Barcelona was ahead at half time in **10** matches, but **3** of those still ended as a draw or loss.

The late-season matches make this particularly visible. Barcelona led Granada 1-0 at half time on April 29 but lost 2-1, led Cádiz 1-0 at half time on February 21 but drew 1-1, and led Levante 2-0 at half time on May 11 but drew 3-3.

Two simple visualizations are included:

- `outputs/figures/result_distribution.png`
- `outputs/figures/goals_by_venue.png`

These findings are descriptive. The sample is too small and deliberately selected around one club, so the analysis should not be generalized to the entire league.

## Future Work

The biggest next step would be expanding the curated sample to all StatsBomb-covered Barcelona league matches for the season and then automating the source extraction directly from the full StatsBomb JSON and football.csv files.

A second improvement would be returning to the original idea of event-level analysis. StatsBomb provides separate event files identified by match ID. Those files would allow the project to calculate shots, expected goals, passes, possession sequences, and other match statistics. That would make it possible to ask stronger questions about *why* Barcelona won or lost instead of only describing score progression.

The original project also proposed FiveThirtyEight SPI forecasts. If a stable archived copy with clear provenance is selected, it could be added as a third source. That would allow the final integrated table to combine pre-match expectation, full-time and half-time results, and event-level performance.

A larger version of the project should also replace the manually reviewed alias dictionary with a documented team-identifier crosswalk. The current alias approach works for a small sample but becomes harder to maintain when multiple leagues and seasons are added.

Finally, the analysis could be extended beyond Barcelona. A league-wide dataset would make comparisons of home advantage, comeback frequency, score consistency, and club-level performance much more meaningful.

## Challenges

The largest challenge was source stability. The original project plan used FiveThirtyEight SPI data, but the live endpoint I had planned to use was no longer a reliable final-project dependency. I decided to change the second source rather than submit a workflow that depended on an unstable URL.

The second challenge was that the sources describe the same real-world matches differently. There is no shared match ID, and team naming conventions differ. This required both syntactic cleaning and semantic alias mapping.

A third challenge was scope. StatsBomb's event-level data is much richer than the match metadata used here, but processing event files would have made the final workflow substantially larger. Since I am completing the project individually, I narrowed the final implementation to a smaller end-to-end workflow that I could actually test and document.

The final limitation is sample size. This repository uses a curated 19-match sample rather than the full league season. I therefore keep the findings descriptive and avoid claims that require statistical generalization.

## Reproducing

The repository includes the input files needed to reproduce the submitted results.

1. Clone or download the repository.
2. Install Python 3.
3. From the project root, install dependencies:

```bash
pip install -r requirements.txt
```

4. Run:

```bash
python run_all.py
```

This executes the cleaning/integration script followed by the analysis script.

The main regenerated artifacts are:

```text
data/processed/integrated_matches.csv
outputs/tables/data_quality_summary.csv
outputs/tables/result_counts.csv
outputs/tables/venue_summary.csv
outputs/tables/halftime_summary.csv
outputs/tables/summary_metrics.json
outputs/figures/result_distribution.png
outputs/figures/goals_by_venue.png
```

The included curated raw CSV files mean the workflow does not require an internet connection to reproduce the submitted analysis.

`scripts/acquire_data.py` is also provided as documentation/code for acquiring the current full upstream files when an internet connection is available. The submitted analysis itself uses the versioned curated inputs in `data/raw/`.

## References

StatsBomb. *StatsBomb Open Data*. GitHub repository. https://github.com/statsbomb/open-data

football.csv. *Cache - Football-Data*. GitHub repository. https://github.com/footballcsv/cache.footballdata

McKinney, W. *pandas: a Foundational Python Library for Data Analysis and Statistics.*

Hunter, J. D. (2007). *Matplotlib: A 2D Graphics Environment*. Computing in Science & Engineering, 9(3), 90-95.
