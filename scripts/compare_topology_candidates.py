#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from analyze_surface_spectrum import analyze as analyze_surface
from analyze_topological_invariant import analyze as analyze_invariant
from analyze_wilson_loop import analyze as analyze_wilson


def locate_required(root: Path, relative_paths: list[str]) -> Path:
    for relative in relative_paths:
        candidate = root / relative
        if candidate.exists():
            return candidate
    raise SystemExit(f"Could not locate any of {relative_paths} in {root}")


def analyze_case(root: Path) -> dict[str, object]:
    invariant = analyze_invariant(locate_required(root, ["invariant.dat", "invariant/invariant.dat"]))
    wilson = analyze_wilson(locate_required(root, ["wilson_loop.dat", "wilson/wilson_loop.dat"]))
    surface = analyze_surface(locate_required(root, ["surface_spectrum.dat", "surface/surface_spectrum.dat"]))
    invariant_penalty = 0.0 if invariant["topology_class"] != "trivial-like" else 2.0
    wilson_penalty = 0.0 if wilson["nontrivial_hint"] else 1.0
    surface_penalty = max(0.0, 0.3 - float(surface["near_fermi_weight"]))
    evidence_score = float(invariant["evidence_score"]) + float(wilson["support_score"]) + float(surface["confidence_score"])
    consistency_penalty = 0.0
    if invariant["topology_class"] == "trivial-like" and (wilson["nontrivial_hint"] or surface["surface_state_hint"]):
        consistency_penalty = 0.5
    elif invariant["topology_class"] != "trivial-like" and not (wilson["nontrivial_hint"] or surface["surface_state_hint"]):
        consistency_penalty = 0.5
    score = invariant_penalty + wilson_penalty + surface_penalty + consistency_penalty
    if evidence_score >= 2.5 and consistency_penalty == 0.0:
        confidence_class = "strong-evidence"
    elif evidence_score >= 1.0:
        confidence_class = "moderate-evidence"
    else:
        confidence_class = "weak-evidence"
    return {
        "case": root.name,
        "path": str(root),
        "topology_class": invariant["topology_class"],
        "nontrivial_keys": invariant["nontrivial_keys"],
        "winding_span": wilson["winding_span"],
        "crossing_count": wilson["crossing_count"],
        "near_fermi_weight": surface["near_fermi_weight"],
        "near_fermi_fraction": surface["near_fermi_fraction"],
        "surface_state_hint": surface["surface_state_hint"],
        "evidence_score": evidence_score,
        "consistency_penalty": consistency_penalty,
        "confidence_class": confidence_class,
        "invariant_penalty": invariant_penalty,
        "wilson_penalty": wilson_penalty,
        "surface_penalty": surface_penalty,
        "screening_score": score,
    }


def analyze_cases(roots: list[Path]) -> dict[str, object]:
    cases = [analyze_case(root) for root in roots]
    ranked = sorted(cases, key=lambda item: item["screening_score"])
    return {
        "ranking_basis": "screening_score = invariant_penalty + wilson_penalty + surface_penalty + consistency_penalty",
        "cases": ranked,
        "best_case": ranked[0]["case"] if ranked else None,
        "observations": [
            "This is a compact topology-screening heuristic intended for ranking candidates, not a full symmetry-based diagnosis."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank topological candidates with a compact invariant-plus-support heuristic.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = analyze_cases([Path(path).expanduser().resolve() for path in args.paths])
    if args.json:
        print(json.dumps(payload, indent=2))
        return
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
