"""
Update script: converts all .ipynb notebooks in the repository to .py (percent format)
using jupytext, placing the results in the _pynotebooks_ directory.

Usage:
    python instructor/scripts/update_pynotebooks.py
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = REPO_ROOT / "_pynotebooks_"

def main():
    notebooks = sorted(REPO_ROOT.rglob("*.ipynb"))
    # Exclude checkpoints and the output directory itself
    notebooks = [
        nb for nb in notebooks
        if ".ipynb_checkpoints" not in str(nb)
        and str(OUTPUT_DIR) not in str(nb.resolve())
    ]

    if not notebooks:
        print("No .ipynb files found.")
        return

    print(f"Found {len(notebooks)} notebooks. Converting to {OUTPUT_DIR}...")

    for nb in notebooks:
        rel = nb.relative_to(REPO_ROOT)
        out_py = (OUTPUT_DIR / rel).with_suffix(".py")
        out_py.parent.mkdir(parents=True, exist_ok=True)

        print(f"  {rel} -> {out_py.relative_to(REPO_ROOT)}")
        subprocess.run(
            [sys.executable, "-m", "jupytext", "--to", "py:percent", "--output", str(out_py), str(nb)],
            check=True,
            capture_output=True,
            text=True,
        )

    print(f"Done! {len(notebooks)} files converted.")

if __name__ == "__main__":
    main()
