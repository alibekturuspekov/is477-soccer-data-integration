from pathlib import Path
import json
import pandas as pd

RAW = Path("data/raw")
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

def load_statsbomb_matches():
    with open(RAW / "statsbomb_la_liga_2020_21_matches.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for m in data:
        rows.append({
            "match_id": m["match_id"],
            "match_date": m["match_date"],
            "home_team": m["home_team"]["home_team_name"],
            "away_team": m["away_team"]["away_team_name"],
            "home_score": m["home_score"],
            "away_score": m["away_score"],
        })
    return pd.DataFrame(rows)

def load_spi():
    df = pd.read_csv(RAW / "spi_matches.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

def main():
    sb = load_statsbomb_matches()
    spi = load_spi()

    spi_2020 = spi[
        (spi["date"] >= "2020-09-01") &
        (spi["date"] <= "2021-06-30")
    ].copy()

    summary = pd.DataFrame([
        {
            "dataset": "StatsBomb La Liga 2020/21",
            "rows": len(sb),
            "columns": len(sb.columns),
            "missing_values": int(sb.isna().sum().sum()),
            "duplicate_rows": int(sb.duplicated().sum()),
        },
        {
            "dataset": "FiveThirtyEight SPI selected date range",
            "rows": len(spi_2020),
            "columns": len(spi_2020.columns),
            "missing_values": int(spi_2020.isna().sum().sum()),
            "duplicate_rows": int(spi_2020.duplicated().sum()),
        },
    ])

    summary.to_csv(OUT / "data_quality_summary.csv", index=False)
    sb.to_csv(OUT / "statsbomb_match_index.csv", index=False)

    print(summary)
    print("\nStatsBomb team names:")
    print(sorted(set(sb["home_team"]) | set(sb["away_team"])))

if __name__ == "__main__":
    main()

