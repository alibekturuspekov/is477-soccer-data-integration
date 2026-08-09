from pathlib import Path
import json
import re
import unicodedata
import pandas as pd

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)

ALIASES = {
    "deportivo alaves": "alaves",
    "atletico madrid": "atletico madrid",
    "real betis": "real betis",
    "celta vigo": "celta vigo",
    "athletic club": "athletic bilbao",
}

def normalize_team(name):
    if pd.isna(name):
        return None
    value = unicodedata.normalize("NFKD", str(name))
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = value.lower()
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return ALIASES.get(value, value)

def load_statsbomb():
    with open(RAW / "statsbomb_la_liga_2020_21_matches.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for m in data:
        rows.append({
            "match_id": m["match_id"],
            "date": m["match_date"],
            "team1": m["home_team"]["home_team_name"],
            "team2": m["away_team"]["away_team_name"],
            "sb_score1": m["home_score"],
            "sb_score2": m["away_score"],
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_spi():
    df = pd.read_csv(RAW / "spi_matches.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df[
        (df["date"] >= "2020-09-01") &
        (df["date"] <= "2021-06-30")
    ].copy()

def main():
    sb = load_statsbomb()
    spi = load_spi()

    for df in (sb, spi):
        df["home_key"] = df["team1"].apply(normalize_team)
        df["away_key"] = df["team2"].apply(normalize_team)

    merged = sb.merge(
        spi,
        how="left",
        on=["date", "home_key", "away_key"],
        suffixes=("_sb", "_spi"),
        indicator=True
    )

    merged["score_agrees"] = (
        (merged["sb_score1"] == merged["score1"]) &
        (merged["sb_score2"] == merged["score2"])
    )

    merged.to_csv(PROCESSED / "integrated_matches.csv", index=False)

    unmatched = merged[merged["_merge"] != "both"]
    unmatched.to_csv(PROCESSED / "unmatched_matches.csv", index=False)

    print(merged["_merge"].value_counts())
    print(f"Integrated file: {PROCESSED / 'integrated_matches.csv'}")
    print(f"Unmatched file: {PROCESSED / 'unmatched_matches.csv'}")

if __name__ == "__main__":
    main()

