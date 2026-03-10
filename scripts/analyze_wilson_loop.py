#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def analyze(path: Path) -> dict[str, object]:
    rows = []
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            rows.append((float(parts[0]), float(parts[1])))
    if not rows:
        raise SystemExit("Wilson-loop file contains no data")
    winding = rows[-1][1] - rows[0][1]
    return {
        "path": str(path),
        "winding_span": winding,
        "max_value": max(value for _, value in rows),
        "min_value": min(value for _, value in rows),
        "observations": ["Wilson-loop winding span extracted from the sampled dataset."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a Wilson-loop dataset.")
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze(Path(args.path).expanduser().resolve())
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
