---
name: "topology-analysis"
description: "Use when the task is to analyze topological quantities from DFT or Wannier-based outputs, including compact topological invariant summaries, Wilson-loop winding summaries, surface-state or arc-spectrum summaries, evidence consistency scoring, candidate ranking, and markdown reports from finished calculations."
---

# Topology Analysis

Use this skill for topology-oriented post-processing rather than generic workflow setup.

## When to use

- summarize a topological invariant result
- inspect Wilson-loop winding output
- summarize a surface-state or Fermi-arc spectrum
- combine invariant, Wilson-loop, and surface evidence into a compact confidence-style screening view
- rank multiple topological candidates with a compact invariant-plus-support heuristic
- write a compact topology-analysis report from existing results

## Use the bundled helpers

- `scripts/analyze_topological_invariant.py`
  Summarize a simple invariant result.
- `scripts/analyze_wilson_loop.py`
  Summarize a Wilson-loop winding dataset.
- `scripts/analyze_surface_spectrum.py`
  Summarize a surface-state or arc spectrum.
- `scripts/compare_topology_candidates.py`
  Rank multiple topological candidates from invariant, Wilson-loop, and surface-spectrum descriptors.
- `scripts/export_topology_report.py`
  Export a markdown topology-analysis report.

## Guardrails

- Do not confuse a single descriptor with a full topological classification.
- State whether the result comes from a band-structure, Wannier, or surface-spectrum source.
- Distinguish raw post-processing output from a full physical interpretation.
