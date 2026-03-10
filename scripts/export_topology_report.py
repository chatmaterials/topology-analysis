#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from analyze_surface_spectrum import analyze as analyze_surface
from analyze_topological_invariant import analyze as analyze_invariant
from analyze_wilson_loop import analyze as analyze_wilson


def screening_note(
    invariant: dict[str, object] | None,
    wilson: dict[str, object] | None,
    surface: dict[str, object] | None,
) -> str:
    if invariant is None and wilson is None and surface is None:
        return "No topology evidence was supplied."
    if invariant is not None and invariant["topology_class"] != "trivial-like":
        if wilson is not None and wilson["nontrivial_hint"] and surface is not None and surface["surface_state_hint"]:
            return "Invariant, Wilson-loop, and surface-spectrum descriptors all point toward a nontrivial topological candidate."
        return "The invariant summary already suggests a nontrivial topology, but the supporting evidence is incomplete."
    if wilson is not None and wilson["nontrivial_hint"]:
        return "Wilson-loop winding suggests a nontrivial candidate even though the supplied invariant summary is weak or absent."
    return "The supplied descriptors look topology-negative or inconclusive in this compact screening view."


def render_markdown(invariant: dict[str, object] | None, wilson: dict[str, object] | None, surface: dict[str, object] | None) -> str:
    lines = ["# Topology Analysis Report", ""]
    if invariant is not None:
        lines.extend(["## Invariants"])
        for key, value in invariant["invariants"].items():
            lines.append(f"- {key}: `{value}`")
        lines.append(f"- Topology class: `{invariant['topology_class']}`")
        lines.append("")
    if wilson is not None:
        lines.extend(
            [
                "## Wilson Loop",
                f"- Winding span: `{wilson['winding_span']:.4f}`",
                f"- Winding direction: `{wilson['winding_direction']}`",
                f"- Crossing count: `{wilson['crossing_count']}`",
                f"- Min / max: `{wilson['min_value']:.4f}` / `{wilson['max_value']:.4f}`",
                "",
            ]
        )
    if surface is not None:
        lines.extend(
            [
                "## Surface Spectrum",
                f"- Peak energy (eV): `{surface['peak_energy_eV']:.4f}`",
                f"- Peak intensity: `{surface['peak_intensity']:.4f}`",
                f"- Near-Fermi weight: `{surface['near_fermi_weight']:.4f}`",
                f"- Surface-state hint: `{surface['surface_state_hint']}`",
                "",
            ]
        )
    lines.extend(["## Screening Note", f"- {screening_note(invariant, wilson, surface)}", ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a markdown topology-analysis report.")
    parser.add_argument("--invariant-path")
    parser.add_argument("--wilson-path")
    parser.add_argument("--surface-path")
    parser.add_argument("--output")
    args = parser.parse_args()
    invariant = analyze_invariant(Path(args.invariant_path).expanduser().resolve()) if args.invariant_path else None
    wilson = analyze_wilson(Path(args.wilson_path).expanduser().resolve()) if args.wilson_path else None
    surface = analyze_surface(Path(args.surface_path).expanduser().resolve()) if args.surface_path else None
    if invariant is None and wilson is None and surface is None:
        raise SystemExit("Provide at least one topology-analysis input")
    output = Path(args.output).expanduser().resolve() if args.output else Path.cwd() / "TOPOLOGY_REPORT.md"
    output.write_text(render_markdown(invariant, wilson, surface))
    print(output)


if __name__ == "__main__":
    main()
