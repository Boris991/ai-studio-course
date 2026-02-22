#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


PLACEHOLDER = "{{url_of_dotenv_file}}"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _iter_notebooks(root: Path) -> list[Path]:
    return sorted(root.rglob("*.ipynb"))


def _escape_for_json_string(value: str) -> str:
    # Produce a JSON-safe string payload without surrounding quotes.
    return json.dumps(value)[1:-1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replace .env download URL placeholder in all notebooks."
    )
    parser.add_argument("url", help="URL to the .env file")
    parser.add_argument(
        "--root",
        default=str(_repo_root()),
        help="Repository root to scan (default: repo root)",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Root path not found: {root}")

    escaped_url = _escape_for_json_string(args.url)

    total = 0
    changed = 0
    for nb_path in _iter_notebooks(root):
        total += 1
        text = nb_path.read_text(encoding="utf-8")
        if PLACEHOLDER not in text:
            continue
        new_text = text.replace(PLACEHOLDER, escaped_url)
        if new_text != text:
            nb_path.write_text(new_text, encoding="utf-8")
            changed += 1

    print(f"Scanned notebooks: {total}")
    print(f"Updated notebooks: {changed}")
    if changed == 0:
        print("No placeholders found to replace.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
