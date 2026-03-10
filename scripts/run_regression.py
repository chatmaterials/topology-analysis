#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=True)


def run_json(*args: str):
    return json.loads(run(*args).stdout)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    invariant = run_json("scripts/analyze_topological_invariant.py", "fixtures/invariant/invariant.dat", "--json")
    ensure(invariant["invariants"]["Z2"] == "1", "topology-analysis should parse the Z2 invariant")
    ensure(invariant["topology_class"] == "z2-nontrivial-like", "topology-analysis should classify the invariant fixture")
    ensure(invariant["evidence_score"] > 0.5, "topology-analysis should compute an invariant evidence score")
    wilson = run_json("scripts/analyze_wilson_loop.py", "fixtures/wilson/wilson_loop.dat", "--json")
    ensure(wilson["winding_span"] > 0.7, "topology-analysis should summarize the Wilson-loop winding span")
    ensure(wilson["nontrivial_hint"], "topology-analysis should identify a nontrivial Wilson hint")
    ensure(wilson["support_score"] > 0.9, "topology-analysis should compute a Wilson support score")
    surface = run_json("scripts/analyze_surface_spectrum.py", "fixtures/surface/surface_spectrum.dat", "--json")
    ensure(abs(surface["peak_energy_eV"] - 0.2) < 1e-6, "topology-analysis should identify the surface-spectrum peak")
    ensure(surface["surface_state_hint"], "topology-analysis should identify near-Fermi surface weight")
    ensure(surface["confidence_score"] > 0.4, "topology-analysis should compute a surface confidence score")
    ranked = run_json("scripts/compare_topology_candidates.py", "fixtures", "fixtures/candidates/ambiguous", "fixtures/candidates/trivial", "--json")
    ensure(ranked["best_case"] == "fixtures", "topology-analysis should rank the nontrivial fixture ahead of the trivial candidate")
    ensure(ranked["cases"][1]["case"] == "ambiguous", "topology-analysis should place the ambiguous candidate between the nontrivial and trivial cases")
    temp_dir = Path(tempfile.mkdtemp(prefix="topology-analysis-report-"))
    try:
        report_path = Path(
            run(
                "scripts/export_topology_report.py",
                "--invariant-path",
                "fixtures/invariant/invariant.dat",
                "--wilson-path",
                "fixtures/wilson/wilson_loop.dat",
                "--surface-path",
                "fixtures/surface/surface_spectrum.dat",
                "--output",
                str(temp_dir / "TOPOLOGY_REPORT.md"),
            ).stdout.strip()
        )
        report_text = report_path.read_text()
        ensure("# Topology Analysis Report" in report_text, "topology report should have a heading")
        ensure("## Invariants" in report_text and "## Wilson Loop" in report_text and "## Surface Spectrum" in report_text, "topology report should include all sections")
        ensure("## Screening Note" in report_text, "topology report should include a screening note")
    finally:
        shutil.rmtree(temp_dir)
    print("topology-analysis regression passed")


if __name__ == "__main__":
    main()
