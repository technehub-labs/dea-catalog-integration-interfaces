#!/usr/bin/env python3
"""Gate 8 (CR-IS-CAT-04B): cross-catalogue reference integrity.

Resolution policy (FOUNDATIONS section 4): references resolve against vendored
target-id snapshots pinned to a commit, never against live fetches at run
time. A service_binding must resolve against the vendored ISS snapshot; a
component_binding must resolve against the vendored ISC snapshot.

This gate also asserts the six anchor records the IS family already depends
on: the five legacy interfaces the ISF and ISC registries reference
(identity-api, api-gateway-public, identity-broker-public,
employee-portal-internal, agent-orchestrator-internal) and the generated
exposure of the identity service (dea:integration-interface-identity-service,
which the ISF registry reference and the ISS record both rely on). If any
disappears, a sibling catalogue's reference goes dark; the failure belongs
here, at the source.

Coverage is asserted in both directions: every exposure the ISS snapshot
declares (its exposed_via ids) must have an IF record, and every IF record id
that appears as an ISS exposure must bind back to the service that declared
it. The five anchors exist outside the ISS population (they are referenced
from the ISF registry, the ISC registry or both) and are covered by the
anchor assertions instead.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
RECORD_GLOB = "entities/v1-alpha/**/interface.yaml"

SNAPSHOT_PATH = REPO / "docs" / "is-semantic-architecture" / "target-id-snapshots.yaml"
ISS_REPO_KEY = "dea-catalog-information-system-services"
ISC_REPO_KEY = "dea-catalog-application-components"

REQUIRED_ANCHORS = (
    "dea:integration-interface-identity-api",
    "dea:integration-interface-api-gateway-public",
    "dea:integration-interface-identity-broker-public",
    "dea:integration-interface-employee-portal-internal",
    "dea:integration-interface-agent-orchestrator-internal",
    "dea:integration-interface-identity-service",
)


def main() -> int:
    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    print(f"Record count: {len(records)}")

    if not SNAPSHOT_PATH.exists():
        print("  - FAIL: docs/is-semantic-architecture/target-id-snapshots.yaml is missing")
        print("Findings: 1")
        return 1

    snap_doc = yaml.safe_load(SNAPSHOT_PATH.read_text(encoding="utf-8")) or {}
    iss_snap = ((snap_doc.get("snapshots") or {}).get(ISS_REPO_KEY)) or {}
    isc_snap = ((snap_doc.get("snapshots") or {}).get(ISC_REPO_KEY)) or {}
    iss_pin = (snap_doc.get("pinned_commits") or {}).get(ISS_REPO_KEY)
    isc_pin = (snap_doc.get("pinned_commits") or {}).get(ISC_REPO_KEY)
    print(f"Snapshot ids ({ISS_REPO_KEY}): {len(iss_snap)}; pinned: {iss_pin}")
    print(f"Snapshot ids ({ISC_REPO_KEY}): {len(isc_snap)}; pinned: {isc_pin}")

    if not iss_pin or not isc_pin:
        print("  - FAIL: both target snapshots must carry a pinned commit (D4)")
        print("Findings: 1")
        return 1

    findings: list[str] = []
    resolved_services = 0
    resolved_components = 0

    present_ids = set()
    service_bindings: dict[str, str] = {}
    for f in records:
        rel = Path(f).relative_to(REPO)
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        rid = doc.get("id") or ""
        present_ids.add(rid)

        sb = doc.get("service_binding") or {}
        cb = doc.get("component_binding") or {}
        if sb.get("service_id"):
            target = sb["service_id"]
            service_bindings[rid] = target
            if target in iss_snap:
                resolved_services += 1
            else:
                findings.append(f"{rel}: service_binding target {target} does not resolve "
                                "against the vendored ISS snapshot")
        if cb.get("component_id"):
            target = cb["component_id"]
            if target in isc_snap:
                resolved_components += 1
            else:
                findings.append(f"{rel}: component_binding target {target} does not resolve "
                                "against the vendored ISC snapshot")

    # Anchor assertions: sibling registries depend on these ids.
    for anchor in REQUIRED_ANCHORS:
        if anchor not in present_ids:
            findings.append(f"anchor record {anchor} is absent; a sibling catalogue "
                            "registry depends on it")

    # Coverage: every ISS exposure must have an IF record, and the record
    # that carries an ISS exposure id must bind back to the declaring service.
    iss_exposures: dict[str, str] = {}
    for sid, entry in iss_snap.items():
        if not isinstance(entry, dict):
            continue
        for ev in entry.get("exposed_via") or []:
            iss_exposures[ev] = sid
    missing = sorted(set(iss_exposures) - present_ids)
    for ev in missing[:40]:
        findings.append(f"exposure {ev} declared by ISS record {iss_exposures[ev]} "
                        "has no IF record")
    if len(missing) > 40:
        findings.append(f"... and {len(missing) - 40} more ISS exposures without IF records")
    for rid, sid in sorted(service_bindings.items()):
        if rid in iss_exposures and iss_exposures[rid] != sid:
            findings.append(f"{rid}: ISS record {iss_exposures[rid]} declares this "
                            f"exposure but the record binds to {sid}")

    print(f"Bindings: {resolved_services} service bindings resolved, "
          f"{resolved_components} component bindings resolved, "
          f"{len(findings)} findings")
    if findings:
        for x in findings[:80]:
            print(f"  - FAIL: {x}")
        if len(findings) > 80:
            print(f"  ... and {len(findings) - 80} more")
    print(f"Findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
