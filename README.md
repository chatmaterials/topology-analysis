# topology-analysis

[![CI](https://img.shields.io/github/actions/workflow/status/chatmaterials/topology-analysis/ci.yml?branch=main&label=CI)](https://github.com/chatmaterials/topology-analysis/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/chatmaterials/topology-analysis?display_name=tag)](https://github.com/chatmaterials/topology-analysis/releases)

Standalone skill for topological-material post-processing, evidence consistency scoring, candidate ranking, and report generation.

## Install

```bash
npx skills add chatmaterials/topology-analysis -g -y
```

## Local Validation

```bash
python3 -m py_compile scripts/*.py
npx skills add . --list
python3 scripts/analyze_topological_invariant.py fixtures/invariant/invariant.dat --json
python3 scripts/analyze_wilson_loop.py fixtures/wilson/wilson_loop.dat --json
python3 scripts/analyze_surface_spectrum.py fixtures/surface/surface_spectrum.dat --json
python3 scripts/compare_topology_candidates.py fixtures fixtures/candidates/ambiguous fixtures/candidates/trivial --json
python3 scripts/export_topology_report.py --invariant-path fixtures/invariant/invariant.dat --wilson-path fixtures/wilson/wilson_loop.dat --surface-path fixtures/surface/surface_spectrum.dat
python3 scripts/run_regression.py
```
