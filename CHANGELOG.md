# Changelog

All notable changes to the Integration Interface catalogue are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Allocation is recorded in the OpenDEAM root model; see `metamodel-pointer.yaml`.

## [Unreleased]

## [0.2.0] - 2026-11-11

### Added

- `CR-IS-CAT-04B`: population. 627 records admitted under `entities/v1-alpha/interfaces/`, derived deterministically from the merged ISS population (one interface per service exposure, 623, including the exposure the ISS record for the API Gateway Service declares) plus the five legacy anchors referenced by the ISF and ISC registries (`dea:integration-interface-identity-api`, `dea:integration-interface-api-gateway-public`, `dea:integration-interface-identity-broker-public`, `dea:integration-interface-employee-portal-internal`, `dea:integration-interface-agent-orchestrator-internal`). Per-system `index.yaml` files. Taxonomy ratified (`docs/TAXONOMY.md`): interface kind derived from the bound service's interaction pattern by a deterministic mapping; consumer class and interaction pattern inherited. Record standard established (`docs/RECORD-STANDARD.md`). Gate 3 extended to validate every record against the schema.
- `scripts/build_target_snapshots.py` and the vendored snapshots (`docs/is-semantic-architecture/target-id-snapshots.yaml`): 623 ISS ids at pinned commit `99ee85017e3b1ae9e77d2f471781791ff942b8c2` (with every service's `exposed_via`), 276 ISC ids at pinned commit `1530a667a9eace490fa3344d9afa32fabfb93e64`.
- Relationship registry with 627 typed `dea:exposes` edges: the bound service or component exposes the interface.
- Gates 6 through 8: taxonomy (one cell per axis, tag mirrors, exactly one binding, duplicate detection on the full identity tuple), evidence (metamodel clause, admitting CR, at least 3 distinct vendor systems, substantive descriptions), reference integrity (bindings resolve against the vendored snapshots, six anchor records present, bidirectional ISS exposure coverage). CI extended to eight steps.
- Pointer `catalog.status` moves to `populated`.

### Changed

- README status table: scaffold to populated, with population method and counts.

### Known issues

- The API catalogue remains pending; the `dea:specifies` edges from API records to IF records will be added by the API catalogue programme, not here.
- `dea-metamodel` entity `dea:IntegrationInterface` still carries the `catalog_repo` contradiction recorded in 0.1.0; a metamodel-side correction remains outstanding.
- ISF, ISC and this repository remain mid-rename against their OpenDEAM allocation. Reference resolution is by identifier, so the renames do not block resolution.

## [0.1.0] - 2026-11-11

### Added

- `CR-IS-CAT-04A`: catalogue foundation. Metamodel pointer pinned to OpenDEAM v0.7.0; rename debt to `dea-catalog-information-system-integration-interfaces` recorded as pending.
- Schema projection of the metamodel IFI entity schema with the catalogue-instance layer (classification axes, bindings, governance).
- `docs/FOUNDATIONS.md`: cardinal scope, classification axes, six admission criteria, cross-catalogue reference policy, repository reality reconciliation, nine-decision register.
- Five CI gates: parse, pointer, schema projection, writing rules, record posture.

### Known issues

- `dea-metamodel` entity `dea:IntegrationInterface` declares `catalog_repo: dea-catalog-api-contracts` while its definition field names `dea-catalog-information-system-integration-interfaces` per CR-IS-CAT-04. This catalogue follows the definition field and records the contradiction; a metamodel-side correction is outstanding.
- ISF, ISC and IF repositories remain mid-rename against their OpenDEAM allocation. Reference resolution is by identifier, so the renames do not block resolution.

### Not in this release

- No records admitted. Population is `CR-IS-CAT-04B`.
- The ISS, ISF and ISC forward references to this catalogue remain correctly declared in their own repositories until the population lands.
