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
        raise SystemExit("Surface-spectrum file contains no data")
    peak = max(rows, key=lambda item: item[1])
    integrated = sum(intensity for _, intensity in rows)
    near_fermi = [(energy, intensity) for energy, intensity in rows if abs(energy) <= 0.1]
    near_fermi_weight = sum(intensity for _, intensity in near_fermi)
    surface_state_hint = near_fermi_weight > 0.0 and near_fermi_weight / integrated >= 0.2 if integrated > 0 else False
    return {
        "path": str(path),
        "peak_energy_eV": peak[0],
        "peak_intensity": peak[1],
        "integrated_intensity": integrated,
        "near_fermi_weight": near_fermi_weight,
        "surface_state_hint": surface_state_hint,
        "observations": ["Surface-spectrum peak summary extracted from the sampled dataset."],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a surface-state or arc spectrum.")
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
