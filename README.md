# Integration Interface

> A defined interaction boundary between an information system (or one of its components) and one or more internal or external consumers or providers, specifying the means, protocols, interaction patterns and contractual constraints through which information or functionality is exchanged.

**Layer:** L5 : **Building block:** L5-integration : **Entity:** `dea:IntegrationInterface` (class alias `IFI`) : **Metamodel:** [v1.0.0](https://github.com/technehub-labs/dea-metamodel)

[![View in Metamodel Explorer](https://img.shields.io/badge/Metamodel%20Explorer-View%20Entity-2C3E50?style=shield)](https://technehub-labs.github.io/metamodel/?entity=IFI)

## Status

**Scaffold.** Established by `CR-IS-CAT-04A` (IF foundation) on 2026-11-11. No records are admitted yet; population is `CR-IS-CAT-04B`.

| Item | State |
|---|---|
| Repository | scaffold, 0 records |
| Metamodel pointer | pinned to OpenDEAM v0.7.0; catalog status `scaffold` |
| Schema projection | landed; three classification axes as first-class fields, bindings and governance in the catalogue-instance layer |
| Population | `CR-IS-CAT-04B` (planned) |

## What this catalogue is

The catalogue of **interaction boundaries**, not of contracts and not of implementations. An IF record specifies the means and shape through which a service contract (ISS) or a component exposure (ISC) is exchanged with consumers. Per the CR-021 D-4 disposition, the interface is distinct from the API contract (`dea:API`) that may specify it via `dea:specifies`.

## What this catalogue is not

| Not this | Why | Where it lives |
|---|---|---|
| A service catalogue | A service names the contract; an interface specifies the means that operationalise it | `dea-catalog-information-system-services` (ISS) |
| A component catalogue | A component encapsulates structure and responsibility; the interface is the boundary it exposes | `dea-catalog-application-components` (ISC) |
| An API catalogue | The API contract artefact specifies a boundary; it is not the boundary itself | API catalogue (pending) |
| An integration runtime | Brokers, gateways and buses are implementations | Vendor evidence only, per G-12 |

## Entity definition

| Field | Value |
|---|---|
| Entity ID | `dea:IntegrationInterface` |
| OpenDEAM entity id | `dea:entity-integration-interface` |
| Class alias | `IFI` |
| Layer | L5 |
| Building block | L5-integration |
| Profile | `dea:digital` |
| Metamodel version | v1.0.0 |
| Status | normative |
| Introducing CR | `dea-metamodel` `CR-021` (D-4 disposition) |
| Legacy ids | `dea:entity-integration-interface` |

## Key tenets

1. **An interface is a boundary, not a contract and not an artefact.** The service contract belongs to ISS; the API contract belongs to the API catalogue. The IF record binds to the contract and specifies the means.
2. **Exactly one binding.** A record carries one `service_binding` or one `component_binding`, never both and never neither. An interface nobody exposes is not a boundary.
3. **The API is a separate entity.** No endpoint, operation or protocol detail appears on a record (D-4/D-6). The API catalogue will relate its records here via `dea:specifies`.
4. **Vendors corroborate, never canonise.** At least 3 distinct vendor systems evidence each boundary; no vendor product is canonical (G-12).
5. **Resolution is against pinned snapshots.** Bindings resolve against vendored ISS and ISC snapshots pinned to a commit (D4); CI never fetches.

## Relationships

| Relationship | IF role | Notes |
|---|---|---|
| `dea:exposes` | target | A service (ISS) or component (ISC) exposes the interface; asserted in the registry by this catalogue at population |
| `dea:specifies` | target | An API contract specifies the interface; owned by the API catalogue |
| `dea:uses` | target | A consumer uses the interface |
| `dea:exchanges` | context | The information or functionality exchanged across the boundary |

Relationship connections are expressed through the relationship registry (`relationships/v1-alpha/relationships.yaml`), not as inline state on the record, per metamodel CR-3.

## Cross-catalogue references

| Catalogue | Allocates | Repository | State |
|---|---|---|---|
| ISS | `dea:InformationSystemService` | `dea-catalog-information-system-services` | populated, 623 records |
| ISC | `dea:InformationSystemComponent` | `dea-catalog-application-components` | populated, 276 records |
| IF | `dea:IntegrationInterface` | `dea-catalog-integration-interfaces` | **scaffold (this repository)** |
| API | `dea:API` | API catalogue | pending |

The ISS population forward-declares 623 exposures to this catalogue under `CR-IS-CAT-04B`; the ISF registry forward-declares `dea:integration-interface-identity-api`; the ISC registry forward-declares four component exposures (`isc-rel-007`, `isc-rel-014`, `isc-rel-102`, `isc-rel-203`). All resolve when `CR-IS-CAT-04B` admits the records. See section 5 of [FOUNDATIONS.md](./docs/FOUNDATIONS.md) for the repository reality reconciliation.

## Repository structure

```
dea-catalog-integration-interfaces/
├── metamodel-pointer.yaml            : entity mapping (do not edit manually)
├── README.md                         : this file
├── CHANGELOG.md
├── docs/
│   ├── FOUNDATIONS.md                : catalogue method + decision-points register
│   ├── TAXONOMY.md                   : the three classification axes (CR-IS-CAT-04B)
│   ├── RECORD-STANDARD.md            : per-record template and evidence bar (CR-IS-CAT-04B)
│   └── is-semantic-architecture/     : vendored snapshots (CR-IS-CAT-04B)
├── schemas/
│   └── integration-interface.schema.json   : catalogue-instance schema projection
├── entities/v1-alpha/interfaces/     : records, one interface.yaml per record (CR-IS-CAT-04B)
├── relationships/v1-alpha/           : relationship registry (CR-IS-CAT-04B)
└── .github/workflows/                : CI gates
```

## Change control

| Artefact | Change authority |
|---|---|
| `metamodel-pointer.yaml` | OpenDEAM root model (`dea-architecture-framework`), never hand-edited |
| `schemas/*.json` | This repository, by CR, mirroring the metamodel |
| `docs/FOUNDATIONS.md` decision register | This repository, by CR |
| `docs/TAXONOMY.md` vocabularies | This repository, by CR against the taxonomy |
| Records under `entities/v1-alpha/` | This repository, by CR, gated on the taxonomy and record standard |
| Allocation of IF to a catalogue | OpenDEAM root model |

## Contributing

Population requires an approved change request. See [docs/FOUNDATIONS.md](./docs/FOUNDATIONS.md) for admission criteria, evidence requirements, and the process a record must follow; see [docs/RECORD-STANDARD.md](./docs/RECORD-STANDARD.md) for what a populated record must contain.
