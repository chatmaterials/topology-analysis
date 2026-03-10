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
    total_variation = sum(abs(y1 - y0) for (_, y0), (_, y1) in zip(rows, rows[1:]))
    crossings = 0
    for (_, y0), (_, y1) in zip(rows, rows[1:]):
        if (y0 - 0.5) == 0 or (y1 - 0.5) == 0 or (y0 - 0.5) * (y1 - 0.5) < 0:
            crossings += 1
    nontrivial_hint = abs(winding) >= 0.5 or crossings > 0
    return {
        "path": str(path),
        "winding_span": winding,
        "winding_direction": "positive" if winding > 0 else ("negative" if winding < 0 else "flat"),
        "total_variation": total_variation,
        "crossing_count": crossings,
        "nontrivial_hint": nontrivial_hint,
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
