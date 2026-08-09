import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

for script in ["scripts/clean_integrate.py", "scripts/analyze.py"]:
    subprocess.run([sys.executable, str(ROOT / script)], check=True)

