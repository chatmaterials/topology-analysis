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
    nontrivial = {}
    for key, value in values.items():
        stripped = value.strip().lower()
        if stripped in {"1", "true", "yes", "nontrivial"}:
            nontrivial[key] = True
            continue
        try:
            nontrivial[key] = abs(float(stripped)) > 1e-12
        except ValueError:
            nontrivial[key] = stripped not in {"0", "false", "no", "trivial"}
    nontrivial_keys = [key for key, flag in nontrivial.items() if flag]
    if any(key.upper() == "CHERN" and nontrivial.get(key, False) for key in values):
        topology_class = "chern-like"
    elif any(key.upper() == "Z2" and nontrivial.get(key, False) for key in values):
        topology_class = "z2-nontrivial-like"
    elif nontrivial_keys:
        topology_class = "nontrivial-like"
    else:
        topology_class = "trivial-like"
    evidence_score = 0.0
    for key in nontrivial_keys:
        if key.upper() == "CHERN":
            evidence_score += 2.0
        elif key.upper() == "Z2":
            evidence_score += 1.0
        else:
            evidence_score += 0.5
    return {
        "path": str(path),
        "invariants": values,
        "nontrivial_keys": nontrivial_keys,
        "topology_class": topology_class,
        "nontrivial_count": len(nontrivial_keys),
        "evidence_score": evidence_score,
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
