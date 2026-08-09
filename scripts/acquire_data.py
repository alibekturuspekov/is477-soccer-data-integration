from pathlib import Path
import hashlib
import json
import requests

RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

STATSBOMB_MATCHES_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/11/90.json"
SPI_URL = "https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv"

def download(url, path):
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    path.write_bytes(r.content)
    return hashlib.sha256(r.content).hexdigest()

def main():
    sb_path = RAW / "statsbomb_la_liga_2020_21_matches.json"
    spi_path = RAW / "spi_matches.csv"

    checksums = {
        str(sb_path): download(STATSBOMB_MATCHES_URL, sb_path),
        str(spi_path): download(SPI_URL, spi_path),
    }

    with open(sb_path, "r", encoding="utf-8") as f:
        matches = json.load(f)

    event_dir = RAW / "statsbomb_events"
    event_dir.mkdir(exist_ok=True)

    for match in matches:
        match_id = match["match_id"]
        url = f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json"
        path = event_dir / f"{match_id}.json"
        checksums[str(path)] = download(url, path)

    with open(RAW / "checksums.json", "w", encoding="utf-8") as f:
        json.dump(checksums, f, indent=2)

    print(f"Downloaded {len(matches)} StatsBomb matches and their event files.")
    print(f"Saved FiveThirtyEight SPI data to {spi_path}.")
    print("SHA-256 checksums saved to data/raw/checksums.json.")

if __name__ == "__main__":
    main()
