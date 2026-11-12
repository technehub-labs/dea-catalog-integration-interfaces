#!/usr/bin/env python3
"""Gate 6 (CR-IS-CAT-04B): record taxonomy conformance.

Ratifies the classification axes of CR-IS-CAT-04B against every record: a
record must occupy exactly one cell per axis; the tag mirrors of the promoted
fields must agree with the fields; duplicate detection operates on the full
identity tuple (system class, binding, three-tuple, offering description
prefix), since the vocabulary sizes make three-tuple collisions among
distinct records mathematically inevitable at population scale (TAXONOMY 3);
and every record must carry exactly one binding: a service_binding to an ISS
record or a component_binding to an ISC record, never both and never neither.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
RECORD_GLOB = "entities/v1-alpha/**/interface.yaml"

INTERFACE_KINDS = {"rest-api", "message-topic", "event-stream", "file-transfer",
                   "rpc", "database-access", "mixed", "other"}
CONSUMER_CLASSES = {"internal-application", "internal-analyst", "internal-machine",
                    "external-partner", "external-customer", "mixed"}
INTERACTION_PATTERNS = {"request-response", "event-push", "event-subscribe",
                        "streaming", "batch", "mixed"}
BINDING_STATUSES = {"bound", "planned", "deprecated"}

AXIS_TAGS = {
    "interface_kind": "interface-kind:",
    "consumer_class": "consumer-class:",
    "interaction_pattern": "interaction-pattern:",
}


def main() -> int:
    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    print(f"Record count: {len(records)}")
    findings: list[str] = []
    seen_cells: dict[tuple, str] = {}

    for f in records:
        rel = Path(f).relative_to(REPO)
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}

        tags = doc.get("tags") or []

        # Promoted first-class fields are primary; their tag mirrors must agree.
        axes = {}
        for field, prefix in AXIS_TAGS.items():
            value = doc.get(field)
            mirrors = [t.split(":", 1)[1] for t in tags if t.startswith(prefix)]
            if len(mirrors) != 1:
                findings.append(f"{rel}: tag mirror {prefix}* must appear exactly once")
            elif mirrors[0] != value:
                findings.append(f"{rel}: {field} is {value!r} but the {prefix} tag "
                                f"mirror says {mirrors[0]!r}")
            axes[field] = value

        if axes["interface_kind"] not in INTERFACE_KINDS:
            findings.append(f"{rel}: interface_kind {axes['interface_kind']!r} is not a "
                            "vocabulary cell of CR-IS-CAT-04B")
        if axes["consumer_class"] not in CONSUMER_CLASSES:
            findings.append(f"{rel}: consumer_class {axes['consumer_class']!r} is not a "
                            "vocabulary cell of CR-IS-CAT-04B")
        if axes["interaction_pattern"] not in INTERACTION_PATTERNS:
            findings.append(f"{rel}: interaction_pattern {axes['interaction_pattern']!r} is not a "
                            "vocabulary cell of CR-IS-CAT-04B")

        systems = [t.split(":", 1)[1] for t in tags if t.startswith("system-class:")]
        if len(systems) != 1:
            findings.append(f"{rel}: system-class tag must appear exactly once")

        # Exactly one binding, and it must be well formed.
        sb = doc.get("service_binding")
        cb = doc.get("component_binding")
        if sb and cb:
            findings.append(f"{rel}: carries both service_binding and component_binding; "
                            "an interface binds to exactly one exposer")
        elif not sb and not cb:
            findings.append(f"{rel}: carries neither service_binding nor component_binding; "
                            "an interface must name the contract or component it operationalises")
        else:
            binding = sb or cb
            key = "service_id" if sb else "component_id"
            if not (binding.get(key) or "").strip():
                findings.append(f"{rel}: binding.{key} is empty")
            if binding.get("binding_status") not in BINDING_STATUSES:
                findings.append(f"{rel}: binding_status {binding.get('binding_status')!r} "
                                "is not a vocabulary cell of CR-IS-CAT-04B")

        # Duplicate detection (TAXONOMY 3, as refined at population scale): the
        # three-tuple classifies, it does not identify. Two records are duplicates
        # only when they share the system class, the binding, the three-tuple and
        # the name. A service may expose more than one boundary; the distinct
        # boundaries of one service share the binding by construction and are
        # distinguished by name (the ISS precedent: the offering text played this
        # role there).
        if systems and (sb or cb):
            binding = sb or cb
            key = "service_id" if sb else "component_id"
            dup_key = (systems[0], key, binding.get(key),
                       axes["interface_kind"], axes["consumer_class"],
                       axes["interaction_pattern"], doc.get("name"))
            if dup_key in seen_cells:
                findings.append(
                    f"{rel}: duplicate of {seen_cells[dup_key]}; same system class, "
                    "binding and three-tuple")
            else:
                seen_cells[dup_key] = str(rel)

    if findings:
        for x in findings[:80]:
            print(f"  - FAIL: {x}")
        if len(findings) > 80:
            print(f"  ... and {len(findings) - 80} more")
        print(f"Findings: {len(findings)}")
        return 1
    print(f"  OK: {len(records)} records occupy exactly one cell per axis; "
          "tag mirrors agree with the promoted fields; one binding per record")
    print("Findings: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
