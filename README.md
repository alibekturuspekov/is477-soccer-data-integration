# IS 477 Soccer Data Integration Project

This repository contains in-progress work for an IS 477 course project on soccer match outcomes.

The project combines:

1. StatsBomb Open Data for detailed La Liga match and event information.
2. FiveThirtyEight Soccer Power Index data for pre-match ratings, probabilities, projected scores, and match results.

The current target is La Liga 2020/2021.

## Current workflow

```bash
pip install -r requirements.txt
python scripts/acquire_data.py
python scripts/profile_data.py
python scripts/integrate_matches.py
```

The workflow is still in development. Event-level aggregation and final analysis will be completed in the next stage.

## Repository structure

- `ProjectPlan.md` - original project plan
- `StatusReport.md` - Milestone 3 interim status report
- `scripts/acquire_data.py` - downloads the two source datasets and StatsBomb event files
- `scripts/profile_data.py` - basic data quality profiling
- `scripts/integrate_matches.py` - first version of match-level integration
- `data/raw/` - source files downloaded by the acquisition script
- `data/processed/` - integrated and unmatched match outputs
- `outputs/` - profiling summaries

## Data sources

StatsBomb Open Data:
https://github.com/statsbomb/open-data

FiveThirtyEight Soccer SPI:
https://github.com/fivethirtyeight/data/tree/master/soccer-spi
