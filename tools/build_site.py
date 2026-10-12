"""Rebuild all static editions in dependency order, with Python's standard library."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

def main():
    for script in ("gen_genre_pages.py", "gen_recommendations.py", "gen_spain.py"):
        subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "tools" / script)], cwd=ROOT, check=True)

if __name__ == "__main__":
    main()
