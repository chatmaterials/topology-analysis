# topology-analysis

Standalone skill for topological-material post-processing and report generation.

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
python3 scripts/export_topology_report.py --invariant-path fixtures/invariant/invariant.dat --wilson-path fixtures/wilson/wilson_loop.dat --surface-path fixtures/surface/surface_spectrum.dat
python3 scripts/run_regression.py
```
