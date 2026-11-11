# Changelog

All notable changes to the Integration Interface catalogue are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Allocation is recorded in the OpenDEAM root model; see `metamodel-pointer.yaml`.

## [Unreleased]

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
