#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def analyze(path: Path) -> dict[str, object]:
    values = {}
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            values[parts[0]] = parts[1]
    return {
        "path": str(path),
        "invariants": values,
        "observations": ["Compact invariant summary extracted from the provided dataset."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a compact topological invariant file.")
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
