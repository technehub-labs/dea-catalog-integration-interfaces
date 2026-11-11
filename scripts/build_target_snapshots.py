#!/usr/bin/env python3
"""Deterministic regenerator for the vendored IF target-id snapshots.

Run locally before opening a PR that touches cross-catalogue references.
Re-commits docs/is-semantic-architecture/target-id-snapshots.yaml with the
harvested ids of the dea-catalog-information-system-services and
dea-catalog-application-components working copies.

Usage: python3 scripts/build_target_snapshots.py [--iss-path PATH] [--isc-path PATH]
                                                     [--iss-pin SHA] [--isc-pin SHA]
  --iss-path PATH   path to a local checkout of dea-catalog-information-system-services
  --isc-path PATH   path to a local checkout of dea-catalog-application-components
  --iss-pin SHA     the commit the ISS working copy represents
  --isc-pin SHA     the commit the ISC working copy represents

This script is the single source of truth for the vendored snapshot. The CI
gate (scripts/check_reference_integrity.py) reads the snapshot YAML and NEVER
re-fetches at run time, so CI is deterministic and offline-safe.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

WORKDIR = Path(__file__).resolve().parent.parent
SNAPSHOT_PATH = WORKDIR / "docs" / "is-semantic-architecture" / "target-id-snapshots.yaml"

ISS_KEY = "dea-catalog-information-system-services"
ISC_KEY = "dea-catalog-application-components"
ISS_GLOB = "service.yaml"
ISC_GLOB = "component.yaml"


def harvest(repo_path: Path, record_glob: str, with_exposures: bool = False) -> dict:
    snap = {}
    for f in sorted((repo_path / "entities").rglob(record_glob)):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(doc, dict) or not doc.get("id"):
            continue
        entry = {
            "name": doc.get("name"),
            "source_file": str(f.relative_to(repo_path)),
        }
        if with_exposures:
            entry["exposed_via"] = doc.get("exposed_via") or []
        snap[doc["id"]] = entry
    return snap


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iss-path", default=str(WORKDIR.parent / ISS_KEY))
    ap.add_argument("--isc-path", default=str(WORKDIR.parent / ISC_KEY))
    ap.add_argument("--iss-pin", default=None)
    ap.add_argument("--isc-pin", default=None)
    args = ap.parse_args()

    iss_repo = Path(args.iss_path)
    isc_repo = Path(args.isc_path)
    if not iss_repo.exists():
        print(f"FAIL: no local {ISS_KEY} checkout found at {iss_repo}")
        return 1
    if not isc_repo.exists():
        print(f"FAIL: no local {ISC_KEY} checkout found at {isc_repo}")
        return 1

    if not args.iss_pin or not args.isc_pin:
        print("FAIL: both pins must be given (--iss-pin, --isc-pin); resolution is "
              "against pinned snapshots (D4), so an unpinned harvest is not admissible")
        return 1

    iss_snap = harvest(iss_repo, ISS_GLOB, with_exposures=True)
    isc_snap = harvest(isc_repo, ISC_GLOB)

    doc = {
        "schema": "dea.if.target-id-snapshots.v1",
        "generated_for": "CR-IS-CAT-04B reference integrity resolution",
        "pinned_commits": {ISS_KEY: args.iss_pin, ISC_KEY: args.isc_pin},
        "snapshots": {ISS_KEY: iss_snap, ISC_KEY: isc_snap},
        "counts": {ISS_KEY: len(iss_snap), ISC_KEY: len(isc_snap)},
    }
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(
        yaml.safe_dump(doc, sort_keys=True, allow_unicode=True), encoding="utf-8")
    print(f"Snapshot written: {len(iss_snap)} ISS ids (pin {args.iss_pin}), "
          f"{len(isc_snap)} ISC ids (pin {args.isc_pin})")
    print(f"Path: {SNAPSHOT_PATH.relative_to(WORKDIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
