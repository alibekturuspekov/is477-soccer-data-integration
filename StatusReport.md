# Milestone 3: Interim Status Report

## Current Status

Since submitting the project plan, I have moved from the planning stage into building the actual data workflow. The project is still focused on soccer and on comparing pre-match expectations with what actually happened during matches. I am continuing with StatsBomb Open Data and FiveThirtyEight’s Soccer Power Index data because the two datasets provide different information that can be connected at the match level.

The original idea was to focus on La Liga 2020/2021, and I have kept that scope for now. I confirmed that StatsBomb’s open-data competition list includes La Liga 2020/2021 as competition ID 11 and season ID 90. I also confirmed that the FiveThirtyEight SPI data includes match date, league, home and away teams, pre-match SPI ratings, win/draw probabilities, projected scores, final scores, and expected-goals fields. This means the basic structure needed for the project is available.

At this point, the main goal of the milestone has been to create a real working structure instead of only having a proposal. The project is not finished, but the acquisition, profiling, and first integration steps now have code in the repository.

## Update on Tasks From the Project Plan

### 1. Confirm datasets and competition

**Status: Completed**

I decided to continue with the two datasets proposed in the original plan:

- StatsBomb Open Data
- FiveThirtyEight Soccer Power Index match data

The current competition is La Liga 2020/2021. I confirmed the StatsBomb competition and season identifiers and reviewed the basic structure of both sources.

The original proposal is available in [ProjectPlan.md](ProjectPlan.md).

### 2. Create repository structure and data organization

**Status: Mostly completed**

I created a basic project structure separating scripts, raw data, processed data, and outputs. My goal is to avoid manually editing source files and to keep the original data separate from anything produced by my own code.

The current structure includes:

- `scripts/` for Python code;
- `data/raw/` for downloaded source data;
- `data/processed/` for integrated results;
- `outputs/` for profiling and later figures/tables.

I also added [README.md](README.md) with a short description of the project and the current workflow.

### 3. Acquire the two datasets

**Status: In progress / initial workflow completed**

I created [scripts/acquire_data.py](scripts/acquire_data.py). The script downloads the StatsBomb La Liga 2020/2021 match file and the FiveThirtyEight SPI match dataset. It also loops through the StatsBomb match IDs and downloads the corresponding event files.

The script records SHA-256 checksums in `data/raw/checksums.json`. I added this because one of the goals of the course is reproducibility and provenance. The checksums give me a way to record the exact files used at the time I ran the project.


### 4. Inspect and profile the data

**Status: In progress**

I created [scripts/profile_data.py](scripts/profile_data.py) to perform an initial quality check. The script looks at row counts, column counts, missing values, and duplicate rows. It also creates a simple match index from the StatsBomb file and prints the team names, which will be useful for integration.

The planned output is `outputs/data_quality_summary.csv`. This is still a basic quality assessment. Later I want to add checks for probability validity, score consistency, missing event files, and duplicate match identifiers.

### 5. Clean and standardize the datasets

**Status: Started**

The biggest cleaning problem I expect is inconsistent team names between the two sources. I created the first version of a normalization function inside [scripts/integrate_matches.py](scripts/integrate_matches.py).

The function converts names to lowercase, removes accents and punctuation, standardizes whitespace, and then applies a small alias dictionary for known naming differences. The alias list is currently incomplete and will be expanded after I inspect unmatched records.

Dates are also converted to a consistent Pandas datetime format before matching.

### 6. Integrate the datasets

**Status: First version completed**

I created an initial match-level integration script in [scripts/integrate_matches.py](scripts/integrate_matches.py).

The current merge uses:

- match date;
- normalized home team;
- normalized away team.

The script keeps StatsBomb’s match ID and combines it with the SPI variables when a matching FiveThirtyEight record is found. It also creates an `unmatched_matches.csv` file so that failed matches can be reviewed instead of silently dropped.

I am starting with exact matching after normalization. Remaining unmatched records will be inspected before I add fuzzy matching.

### 7. Create match-level event statistics

**Status: Not yet completed**

This will be the next major technical step. StatsBomb’s event files contain much more detailed information than the match file. I plan to aggregate those records to the match/team level and calculate a smaller set of useful variables such as shots, shots on target, expected goals, pass completion, and a possession-related measure.

I have not completed this part yet because I wanted to first make sure the two match-level sources can be acquired and linked correctly.

### 8. Analysis and visualizations

**Status: Not started**

The final analysis has not been completed yet. Once the event data is aggregated and merged, I will classify the pre-match favorite using the SPI probabilities and compare games where the favorite won with games where the favorite drew or lost.

The final visualizations will compare forecast probability with actual results and match statistics between expected and unexpected outcomes.

### 9. Reproducibility and final workflow

**Status: In progress**

The scripts are being written so that the project can eventually be run from raw data to final output without manually changing the datasets. I added [requirements.txt](requirements.txt) to document the Python dependencies.

A final `run_all.py` script is still planned but has not been created yet. I will add it after the individual scripts are stable.

## Updated Timeline

| Task | Status | Updated Completion |
|---|---|---|
| Confirm datasets and competition | Completed | Completed |
| Repository organization | Mostly completed | Milestone 3 |
| Data acquisition code | Initial version completed | Milestone 3 |
| Initial data quality profiling | In progress | Milestone 3 / next work session |
| Team-name cleaning and mapping | Started | Next work session |
| Match-level dataset integration | First version completed | Next work session |
| Event-level extraction and aggregation | Not started | After integration check |
| Expanded quality assessment | Not started | After event aggregation |
| Analysis and visualizations | Not started | Final project stage |
| End-to-end automation | In progress | Final project stage |
| Final documentation | Not started | Final project stage |

## Changes From the Original Project Plan

The overall project question and datasets have not changed. The main change is that I am treating the integration as a more gradual process than I originally expected. Instead of immediately using fuzzy matching, I am first normalizing names, attempting an exact composite-key match, and saving unmatched records for inspection.

I also reduced the number of event-level metrics I am committing to at this stage. The original plan listed several possible measures. I still want to use expected goals, shots, passing, and possession-related information, but I will only keep variables that I can calculate consistently and explain clearly.

This is mainly a scope decision. Since I am working individually, I would rather have a smaller reproducible pipeline than a large analysis with several unfinished pieces.

## Challenges and Plans to Address Them

The first challenge is that the datasets use different schemas and file formats. StatsBomb uses nested JSON, while FiveThirtyEight uses a tabular CSV. I addressed the first part by writing separate acquisition and loading logic rather than trying to force both files into the same structure immediately.

The second challenge is match identification. The sources do not share a universal match ID. My current solution is a composite key using date, home team, and away team after name normalization. Any unmatched records will be written to a separate file and reviewed.

The third challenge is the size and complexity of the StatsBomb event data. Each match has its own event file, so the final aggregation has to process many nested JSON records. My plan is to build one match-level aggregation function, test it on a small number of games, and then run it across the full set.

Another challenge is keeping the project realistic within the remaining time. I have therefore kept the research question narrow and am prioritizing data integration, quality, and reproducibility before adding more advanced analysis.

## Individual Contribution

I am completing the project individually with course approval, so all work in this milestone is my contribution. For this milestone I finalized the data sources and competition, created the repository structure, wrote the first acquisition and profiling scripts, started the cleaning rules, created the first match-integration workflow, documented dependencies, and wrote this status report.

The next priority is to run and validate the workflow, inspect unmatched matches, aggregate the StatsBomb event data, and then move into the final analysis.
